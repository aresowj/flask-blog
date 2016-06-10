# -*- coding: utf-8 -*-

"""App initialization part, registering global
methods or procedures to the app instance.
"""

import logging
from app import app


logger = logging.getLogger(__name__)


@app.teardown_request
def close_session(exception=None):
    if not exception:
        app.db.session.commit()
        app.db.remove_current_session()
    else:
        app.db.roll_back_current_session()
        app.db.remove_current_session()
        app.db.dispose_pool()


import views
