#!/usr/bin/env python

# Copyright 2011 Thierry Carrez <thierry@openstack.org>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import simplejson as json
import os
import sys
import time
from jinja2 import Environment, FileSystemLoader
from launchpadlib.launchpad import Launchpad


def create_files(templatepath, outputpath, projects):
    # Create index file
    env = Environment(loader=FileSystemLoader(templatepath))
    indexfile = os.path.join(outputpath, "index.html")
    if not os.path.exists(indexfile):
        template = env.get_template('index.html')
        template.stream(projects=projects).dump(indexfile)

    # Create each project file
    for project in projects:
        projectfile = os.path.join(outputpath, "%s.html" % project['project'])
        if not os.path.exists(projectfile):
            if 'height' in project:
                project['height'] = project['height'] - 30
            template = env.get_template('project.html')
            template.stream(project=project).dump(projectfile)


def update_stats(outputpath, project_name, rotation):

    now = int(time.time())
    records = []
    counts = {}
    project = launchpad.projects[project_name]
    project_stats_filename = os.path.join(outputpath,
                                 "%s-bug-stats.json" % (project_name))

    try:
        data_file = open(project_stats_filename, 'r')
        json_data = json.load(data_file)
        data_file.close()
        for record in json_data['records']:
            if rotation:
                if (now - record['date']) > (rotation * 24 * 60 * 60):
                    print "skip"
                    continue
            records.append(record)
    except IOError:
        pass

    open_statuses = ["New", "Incomplete", "Incomplete (with response)",
                     "Incomplete (without response)", "Confirmed", "Triaged",
                     "In Progress"]

    closed_statuses = ["Fix Committed", "Fix Released", "Invalid", "Won't Fix"]

    importances = ["Undecided", "Wishlist", "Low", "Medium", "High",
                   "Critical"]

    open_tasks = project.searchTasks(status=open_statuses,
                                     order_by='-datecreated',
                                     omit_duplicates=True)
    open_tasks_count = int(
                       open_tasks._wadl_resource.representation['total_size'])

    counts['date'] = now

    if open_tasks_count != 0:
        for open_status in open_statuses:
            if open_status == 'Incomplete':
                status_count = int(
                    project.searchTasks(
                        status=['Incomplete (with response)',
                                'Incomplete (without response)'],
                        omit_duplicates=True
                    )._wadl_resource.representation['total_size'])
            else:
                status_count = int(
                    project.searchTasks(
                        status='%s' % open_status,
                        omit_duplicates=True
                    )._wadl_resource.representation['total_size'])
            status_key = open_status.replace(" ", "").lower()
            status_key = status_key.replace("(", "-")
            status_key = status_key.replace(")", "")
            counts[status_key] = status_count

    elif open_tasks_count == 0:
        for open_status in open_statuses:
            status_key = open_status.replace(" ", "").lower()
            counts[status_key] = 0

    for closed_status in closed_statuses:
        status_count = int(
            project.searchTasks(
                status='%s' % closed_status,
                omit_duplicates=True
            )._wadl_resource.representation['total_size'])
        status_key = closed_status.replace(" ","").replace("'","").lower()
        counts[status_key] = status_count

    for importance in importances:
        importance_count = int(
            project.searchTasks(
                importance='%s' % importance,
                omit_duplicates=True
            )._wadl_resource.representation['total_size'])
        counts[importance.lower()] = importance_count

    records.append(counts)

    report = {
              'keys': ['date', 'new', 'incomplete', 'confirmed', 'triaged',
                       'inprogress', 'fixcommitted', 'fixreleased', 'invalid',
                       'wontfix', 'undecided', 'wishlist', 'low', 'medium',
                       'high', 'critical'],
              'records': records
             }

    project_stats_file = open(project_stats_filename, 'w')
    project_stats_file.write(json.dumps(report, indent=4))
    project_stats_file.close()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print >> sys.stderr, "No directory supplied"

    basepath = os.path.dirname(sys.argv[0])
    configpath = os.path.join(basepath, "config.js")
    templatepath = os.path.join(basepath, "templates")
    outputpath = sys.argv[1]
    if not os.path.isdir(outputpath):
        print >> sys.stderr, '%s is not a directory' % outputpath
        sys.exit(1)

    if not os.path.isfile(configpath):
        print >> sys.stderr, '%s does not contain config.js' % basepath
        sys.exit(1)

    cachedir = os.path.expanduser("~/.launchpadlib/cache/")
    if not os.path.exists(cachedir):
        os.makedirs(cachedir, 0700)

    with open(configpath, 'r') as configfile:
        config = json.load(configfile)
    projects = config['projects']
    rotation = config.get('rotation')

    # Create files in output directory, if needed
    create_files(templatepath, outputpath, projects)

    # Refresh JSON stats files
    launchpad = Launchpad.login_anonymously('bugdaystats', 'production',
                                            cachedir)

    for p in projects:
        update_stats(outputpath, p['project'], rotation)
