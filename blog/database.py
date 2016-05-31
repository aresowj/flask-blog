# -*- coding: utf-8 -*-

"""Definitions for database controller
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from blog import config


logger = logging.getLogger(__name__)


class Database(object):
    _app = None
    _session_class = None
    _current_session = None
    _db_engine = None

    def __init__(self, app):
        self._app = app

    def set_db_engine(self):
        self._db_engine = create_engine(config.SQLALCHEMY_DATABASE_URI,
                                        encoding=config.DB_CHARSET,
                                        pool_recycle=3600,
                                        pool_size=500,
                                        echo=config.DEBUG)

    @property
    def db_engine(self):
        if not self._db_engine:
            self.set_db_engine()

        return self._db_engine

    @property
    def db_session_class(self):
        if self._session_class is None:
            self.update_db_session_class()

        return self._session_class

    def update_db_session_class(self):
        self._session_class = scoped_session(sessionmaker(bind=self.db_engine))

    @property
    def session(self):
        if self._current_session is None:
            self._current_session = self.db_session_class()

        return self._current_session

    def dispose_pool(self):
        """Call this function to dispose all connections in the pool
        when exception occurs"""
        self._db_engine.dispose()

    def remove_current_session(self):
        if not self._current_session:
            return True

        try:
            self._session_class.remove()
        except Exception as e:
            logger.error("Could not remove current session.")
            logger.exception(e)
            raise e
        else:
            self._current_session = None
            return True

    def roll_back_current_session(self):
        if not self._current_session:
            return True
        else:
            self._current_session.rollback()
