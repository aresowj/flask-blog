# -*- coding: utf-8 -*-

"""Definitions for database controller
"""

import logging


logger = logging.getLogger(__name__)


class Database(object):
    _session_class = None
    _current_session = None

    def __init__(self, session_class):
        self._session_class = session_class

    @property
    def session(self):
        if self._current_session is None:
            self._current_session = self._session_class()

        return self._current_session

    def close_current_session(self):
        if not self._current_session:
            return True

        try:
            self._current_session.commit()
            self._current_session.flush()
            self._current_session.close()
        except Exception as e:
            logger.exception(e)
            raise e
        else:
            self._current_session = None
            return True
