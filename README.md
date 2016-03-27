# flask-blog
A small blog app written with Flask, Bootstrap and JQuery.
Still under building, category and search function to be added.

Author: Ares Ou

####  Database Initialization

This micro blog is using flask-migration to manage the migration of database.
Use this command to initialize the plugin:

`python manage.py db init`

After successfully initialized the migration, use this command to create tables for the blog:

`python manage.py db upgrade`

