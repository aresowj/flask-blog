# -*- coding: utf-8; -*-

import logging
from local_settings import *


##################################################
#         local_settings.py example
#
# DB_USER_NAME = 'user'
# DB_PASSWORD = 'password'
# DB_HOST_NAME = 'localhost'
# DB_DATABASE_NAME = 'database'
# DB_CHARSET = 'utf8'
# SERVER_ADDRESS = '0.0.0.0'
# SERVER_PORT = 7000
# DEBUG = True
#
##################################################

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER_NAME + ':' + DB_PASSWORD + \
                    '@' + DB_HOST_NAME + '/' + DB_DATABASE_NAME + '?charset=' + DB_CHARSET

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

POSTS_PER_PAGE = 10
MIN_PASSWORD_LENGTH = 8
DEFAULT = None      # this is for flask-script turning on the debug option

# global strings
ABOUT_TITLE = 'About'
BLOG_NAME = 'Crayon Kingdom'
BLOG_AUTHOR = 'Ares Ou'
BLOG_DESCRIPTION = 'A tech, develop and reading blog.'
NEW_POST_PAGE_TITLE = 'New Post'
NEW_POST_PAGE_HEADER = 'New Post'
EDIT_POST_PAGE_TITLE = 'Edit Post'
EDIT_POST_PAGE_HEADER = 'Edit Post'
LOGIN = 'Login'
LOGIN_PAGE_DESCRIPTION = ''
LOGIN_SUCCEED = 'Login succeed.'
LOGIN_FAILED_USER_NOT_EXIST = 'Login failed, no such user. Please confirm your username.'
LOGIN_FAILED_DUPLICATED_USER = 'Login failed, duplicate username found, please contact admin!'
LOGIN_FAILED_PASSWORD_NOT_MATCH = 'Login failed, password not matched, please try again.'
REGISTRATION = 'Sign up'
REGISTRATION_NOT_ALLOWED = 'Registration is disabled at this time.'
REGISTRATION_PAGE_DESCRIPTION = 'Please enter your information'
REGISTRATION_SUCCEED = 'Registered successfully! You can login now.'
REGISTRATION_FAILED = 'Registration failed, please contact admin.'
FIRST_PAGE = 'First'
PREVIOUS_PAGE = 'Previous'
NEXT_PAGE = 'Next'
LAST_PAGE = 'Last'
POST_ADD_SUCCEED = 'New post successfully added.'
POST_EDIT_SUCCEED = 'Post successfully edited.'
POST_DELETE_SUCCESS = 'Post deleted.'
POST_DELETE_FAILED = 'Post deletion failed.'
PERMISSION_NOT_LOGGED_IN = 'You must be logged in first.'
PERMISSION_NOT_HAVE = 'Sorry, you do not have permission.'
FORM_ERROR = 'There\'s some error in your form.'

# End point names
END_POINT_INDEX = 'index'
END_POINT_ABOUT = 'about'
END_POINT_LOGIN = 'login'
END_POINT_LOGOUT = 'logout'
END_POINT_ADMIN_POST_LIST = 'admin_post_list'
END_POINT_ADMIN_POST_EDIT = 'admin_post_edit'
END_POINT_ADMIN_POST_DELETE = 'admin_delete_post'
END_POINT_ADMIN_CATEGORY_LIST = 'admin_categories_list'
END_POINT_SIGN_UP = 'sign_up'
END_POINT_POST_VIEW = 'post_view'

# Other keys
SESSION_KEY_USERNAME = 'username'
SESSION_KEY_IS_ADMIN = 'is_admin'
