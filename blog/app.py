# -*- coding: utf-8 -*-

import logging
from flask import Flask
import config
from database import Database


logger = logging.getLogger(__name__)
# initialize app
app = Flask(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object(config)
app.db = Database(app)
