# flask-blog
A small blog app written with Flask, Bootstrap and JQuery.
Still under building, category and search function to be added.

Latest Release: **v0.0.3** (May 29th, 2016)
Author: Ares Ou

####  Database Initialization

This micro blog is using flask-migration to manage the migration of database.
Use this command to initialize the plugin:

`python manage.py db init`

After successfully initialized the migration, use this command to create tables for the blog:

`python manage.py db upgrade`


####  Start Development Server

After setting up paraemters in `local_settings.py`, you can use below command to start the dev server:

    cd blog/
    python wsgi.py

#### Coverage Status (as per 06/22/2016)

| Module                 | statements | missing | excluded | coverage |
|------------------------|------------|---------|----------|----------|
| blog/app.py            | 21         | 3       | 0        | 86%      |
| blog/config.py         | 51         | 1       | 0        | 98%      |
| blog/database.py       | 46         | 25      | 0        | 46%      |
| blog/forms.py          | 28         | 3       | 0        | 89%      |
| blog/local_settings.py | 9          | 0       | 0        | 100%     |
| blog/models.py         | 194        | 98      | 0        | 49%      |
| blog/unit_tests.py     | 154        | 4       | 0        | 97%      |
| blog/utilities.py      | 49         | 5       | 0        | 90%      |
| blog/views.py          | 81         | 13      | 0        | 84%      |
| **Total**                 | **633**        | **152**     | **0**        | **76%**      |
