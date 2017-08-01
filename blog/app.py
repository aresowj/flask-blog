# -*- coding: utf-8 -*-

"""App initialization part, registering global
methods or procedures to the app instance.
"""

import logging
import markdown2
from flask import Flask, Markup
from blog import config
from blog.database import Database
from blog.models import Tag, Category, fetch_all_instances


logger = logging.getLogger(__name__)
# initialize app
app = Flask(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object(config)
app.db = Database(app)
app.config['post_tags'] = {}
app.config['categories'] = []


@app.teardown_request
def close_session(exception=None):
    if not exception:
        app.db.session.commit()
        app.db.remove_current_session()
    else:
        app.db.roll_back_current_session()
        app.db.remove_current_session()
        app.db.dispose_pool()


@app.before_first_request
def init_app():
    # get some global objects
    # create tag dictionary for app-wide use
    if not app.config['post_tags']:
        for tag in Tag.get_all_tags():
            app.config['post_tags'][tag.name] = tag.id

    if not app.config['categories']:
        app.config['categories'] = Category.fetch_all_categories()


@app.template_filter('parse_markdown')
def parse_markdown(markdown_text):
    return Markup(markdown2.markdown(markdown_text))
