Bug Day Stats page generator
============================

The ``bugdaystats.py`` script is used to extract data from Launchpad
and produce static HTML that shows progress during a Bug Day.

Usage
-----

``python3 bugdaystats.py output``

``output`` is the name of the directory you will generate data
and HTML files to (if they don't exist yet). It should contain a
``js`` subdirectory containing JavaScript include files, but
otherwise be empty. In addition, it can contain two types of data
files. One file contains data in each time when running the script,
and another one is created daily. That means the creation is skipped
if the previous data is in the same day. The data file is useful for
showing long-term bug situation.

You'll need to run the script at least twice to generate enough
stats to get a graph.

Stats are updated every time the script is run. You should run
``bugdaystats.py`` regularly over the course of your bugday.

Configuration
-------------

The ``config.js`` configuration file describes the projects you want
to generate data for. An example ``config.js.sample`` file is provided
that may be renamed and modified to suite your needs.

``height`` is an optional parameter detailing
the size of the graph (230 pixels is the default value). ``title``
is an optional parameter for the name of the project in the index
page.

You can also optionally specify a ``rotation`` parameter. Entries older
than the value (in days) will be removed from the dataset, resulting
in a rolling view of bug activity.

And you can also optionally specify a ``daily`` parameter to enable the
feature of daily data collection and showing its graphs.
``daily_rotation`` parameter is for daily data collection feature but
it is same as ``rotation`` parameter.
