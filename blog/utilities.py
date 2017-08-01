# -*- coding: utf-8; -*-

"""Global utilities for reuse."""


from functools import wraps
from math import ceil
from flask import session, redirect, url_for, flash
from wtforms import ValidationError
from blog import config
from blog.models import User


def password_strength(form, field):
    """
    helper function for edit or registration form, validating password field
    :param form: passed from WTForms
    :param field: passed from WTForms
    :return: nothing
    """
    if len(field.data) < config.MIN_PASSWORD_LENGTH:
        raise ValidationError('Password must be longer than %d characters' %
                              config.MIN_PASSWORD_LENGTH)
    if field.data.isnumeric() or field.data.isalpha():
        raise ValidationError('Password must contain at least one letter \
                                 and one number!')


def user_exists(form, field):
    """
    helper function for registration form, check if email has been occupied.
    :param form: passed from WTForms
    :param field: passed from WTForms
    :return: nothing
    """
    user = User.get_user_by_email(field.data)

    if user is not None:
        raise ValidationError('This email has already been registered.')


def login_required():
    """A decorator to require user authentication."""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get(config.SESSION_KEY_USERNAME, None):
                flash(config.PERMISSION_NOT_LOGGED_IN, 'error')
                return redirect(url_for(config.END_POINT_LOGIN))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def admin_required():
    """A decorator to require admin user authentication."""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get(config.SESSION_KEY_IS_ADMIN, False):
                flash(config.PERMISSION_NOT_HAVE, 'error')
                return redirect(url_for(config.END_POINT_INDEX))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


class Pagination(object):
    """Class to model the general pagination."""
    def __init__(self, page, show_per_page, total_count):
        self.page = page
        self.show_per_page = show_per_page
        self.total_count = total_count

    @property
    def pages(self):
        """Return the count of pages in current instance"""
        return int(ceil(self.total_count / float(self.show_per_page)))

    @property
    def has_previous(self):
        """Return if current page has previous page."""
        return self.page > 1

    @property
    def has_next(self):
        """Return if current page has next page."""
        return self.page < self.pages

    def iter_pages(self, side_count=5):
        """An iterator to return a list of page numbers."""
        start = self.page - side_count if self.page > side_count else 1
        end = (self.pages if self.page + side_count >= self.pages
               else self.page + side_count)
        for i in range(start, end + 1):
            yield i
