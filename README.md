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

#### Coverage Status (as per 06/08/2016)

| Module                 | statements | missing | excluded | coverage |
|------------------------|------------|---------|----------|----------|
| Total                  | 484        | 227     | 0        | 53%      |
| blog/app.py            | 9          | 0       | 0        | 100%     |
| blog/config.py         | 39         | 1       | 0        | 97%      |
| blog/database.py       | 46         | 25      | 0        | 46%      |
| blog/forms.py          | 29         | 7       | 0        | 76%      |
| blog/local_settings.py | 9          | 0       | 0        | 100%     |
| blog/models.py         | 182        | 107     | 0        | 41%      |
| blog/unit_tests.py     | 39         | 13      | 0        | 67%      |
| blog/utilities.py      | 52         | 26      | 0        | 50%      |
| blog/views.py          | 79         | 48      | 0        | 39%      |
