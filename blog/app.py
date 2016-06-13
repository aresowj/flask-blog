# -*- coding: utf-8 -*-

"""App initialization part, registering global
methods or procedures to the app instance.
"""

import logging
import markdown2
from flask import Flask, Markup
import config
from database import Database


logger = logging.getLogger(__name__)
# initialize app
app = Flask(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object(config)
app.db = Database(app)


@app.teardown_request
def close_session(exception=None):
    if not exception:
        app.db.session.commit()
        app.db.remove_current_session()
    else:
        app.db.roll_back_current_session()
        app.db.remove_current_session()
        app.db.dispose_pool()


@app.template_filter('parse_markdown')
def parse_markdown(markdown_text):
    return Markup(markdown2.markdown(markdown_text))
