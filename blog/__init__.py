import logging
from flask import Flask, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import config
from .database import Database

logger = logging.getLogger(__name__)

# initialize app
app = Flask(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object(config)
# initialize database connection
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], encoding=app.config['DB_CHARSET'], echo=True)
app.db_engine = db_engine
DBSession = sessionmaker(bind=db_engine)  # bind engine to session object
app.db = Database(DBSession)


@app.after_request
def close_session(response=None):
    if not app.db.close_current_session():
        logger.error("Could not close current session.")
    return response

import blog.views
