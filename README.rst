Bug Day Stats page generator
============================

The bugdaystats.py script is used to extract data from Launchpad
and produce static HTML that shows progress during a Bug Day.

Prerequisites
-------------

You'll need the following Python modules installed:
 - launchpadlib
 - jinja2

Usage
-----

python bugdaystats.py output

'output' is the name of the directory you will generate data
and HTML files to (if they don't exist yet). It should contain a
'js' subdirectory containing JavaScript include files, but
otherwise be empty.

You'll need to run the script at least twice to generate enough
stats to get a graph.

Stats are updated every time the script is run. You should run
bugdaystats.py regularly over the course of your bugday.

Configuration
-------------

The config.js configuration file describes the projects you want
to generate data for. "height" is an optional parameter detailing
the size of the graph (230 pixels is the default value). "title"
is an optional parameter for the name of the project in the index
page.
