# -*- coding: utf-8 -*-

"""flask-blog unit tests
"""


import unittest
from unittest import mock
from flask import session, Response, url_for, request
from flask_api import status as http_status
from werkzeug.security import generate_password_hash
from wtforms import ValidationError
import app as app_module
import config
import views as views_module
from models import Post, Authentication, User
from forms import LoginForm
from utilities import password_strength


__author__ = 'Ares Ou'


TEST_POST_TITLE = 'Test Post for Unit Test'
TEST_POST_CONTENT = ''
TEST_USER_NAME = 'admin'
TEST_USER_PASSWORD = 'admin'
TEST_USER_EMAIL = 'admin@admin.com'

app = app_module.app

test_post = Post()
test_post.title = TEST_POST_TITLE
test_post.content = TEST_POST_CONTENT

test_admin_user = User()
test_admin_user.password = generate_password_hash(TEST_USER_PASSWORD, method='pbkdf2:sha256')
test_admin_user.email = TEST_USER_EMAIL
test_admin_user.name = TEST_USER_NAME
test_admin_user.is_admin = True


def return_login_form(user):
    form = LoginForm()
    form.username.data = user.email
    form.password.data = TEST_USER_PASSWORD
    form.remember.data = True
    return form


class UnitTestBase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost'
        app.db = mock.Mock()
        self.client = app.test_client()


class ViewsUnitTest(UnitTestBase):
    def test_index(self):
        with mock.patch('models.Post.get_posts', return_value=([], 0)), \
             mock.patch('utilities.Pagination', return_value=[]), \
             app.app_context():
            response = self.client.get(url_for(config.END_POINT_INDEX))
            # assert got response
            self.assertIsInstance(response, Response)
            # assert get OK
            self.assertEqual(response.status_code, http_status.HTTP_200_OK)
            # assert blog name is in the index page
            self.assertIn(bytes(config.BLOG_NAME, encoding='utf-8'), response.data)

    def test_admin_post_list(self):
        with mock.patch('models.Post.get_posts', return_value=([], 0)), \
             mock.patch('utilities.Pagination', return_value=[]), \
             app.app_context():
            response = self.client.get(url_for(config.END_POINT_ADMIN_POST_LIST))
            # not logged in, the user should be redirected to the index page,
            # thus a status code of 302 is returned.
            self.assertEqual(response.status_code, http_status.HTTP_302_FOUND)
            # login as admin and test again
            with mock.patch('models.User.get_user_by_email', return_value=test_admin_user):
                response = self.client.post(url_for(config.END_POINT_LOGIN), data={
                    'username': TEST_USER_EMAIL,
                    'password': TEST_USER_PASSWORD
                }, follow_redirects=True)
                self.assertEqual(response.status_code, http_status.HTTP_200_OK)

    def test_admin_category_list(self):
        pass

    def test_post_view(self):
        pass

    def test_post_edit(self):
        pass

    def test_delete_post(self):
        pass

    def test_login(self):
        pass

    def test_logout(self):
        pass

    def test_sign_up(self):
        pass

    def test_about(self):
        pass


class UtilitiesUnitTest(UnitTestBase):
    def test_parse_markdown(self):
        pass

    def test_password_strength(self):
        field = mock.Mock()
        form = mock.Mock()

        with self.assertRaises(ValidationError):
            field.data = 't' * (config.MIN_PASSWORD_LENGTH - 1)
            # password length should meet requirement
            password_strength(form, field)

        # password length should contain both alphabets and numbers
        with self.assertRaises(ValidationError):
            field.data = 't' * config.MIN_PASSWORD_LENGTH
            password_strength(form, field)

        with self.assertRaises(ValidationError):
            field.data = 't' * config.MIN_PASSWORD_LENGTH
            password_strength(form, field)
        
        field.data = 't' * (config.MIN_PASSWORD_LENGTH - 1) + '1'
        try:
            password_strength(form, field)
        except ValidationError:
            self.fail('password_strength() is not passing a valid password: %s' % field.data)


class APIUnitTest(UnitTestBase):
    def test_api_available_tags(self):
        pass


class DataBaseClassUnitTest(UnitTestBase):
    pass


class FormsUnitTest(UnitTestBase):
    def test_custom_tag_input_field(self):
        pass


class ModelUnitTest(UnitTestBase):
    pass


if __name__ == '__main__':
    # run_tests(locals())
    unittest.main()
