Descartes-bi
=============

Descartes-bi is a database agnostic, Django based business intelligence tool.

![screenshot](https://raw.github.com/rosarior/descartes-bi/master/docs/_static/screenshot.png)

Implementation
--------------

Descartes-bi encapsulates small snipets of SQL in pseudo-objects called series, that can later be combined to create comparative charts.  Aside from containing series, charts can also define parameters for user interaction.  Parameters (called filters) can be programmed to be restrictive using a custom permission system.


Requirements
------------

 * Django 1.5.x


Setting up
----------

By default the project is set up to run on a SQLite database. Run::

    $ python manage.py syncdb --migrate


Executing
---------

Use:

    $ python manage.py runserver



Creating charts
---------------

Go into the admin site and start creating SQL queries to extract data from your data source DB and combine them into different charts.

License
-------
Descartes-bi is licensed under the terms of the GNU License version 3, see the included LICENSE file.
