# -*- coding: utf-8 -*-

"""flask-blog unit tests
"""


import unittest
from flask_api import status as http_status
from unittest import mock
from app import app
import config
import views


__author__ = 'Ares Ou'


class UnitTestBase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()


class ViewsUnitTest(UnitTestBase):
    def test_index(self):
        with mock.patch('models.Post.get_posts', return_value=([], 0)), \
             mock.patch('utilities.Pagination', return_value=[]):
            response = self.client.get(config.PATH_INDEX)
            # assert blog name is in the index page
            self.assertEqual(response.status_code, http_status.HTTP_200_OK)
            self.assertIn(bytes(config.BLOG_NAME, encoding='utf-8'), response.data)

    def test_admin_post_list(self):
        with mock.patch('models.Post.get_posts', return_value=([], 0)), \
             mock.patch('utilities.Pagination', return_value=[]):
            response = self.client.get(config.PATH_POST_LIST)
            # not logged in, the user should be redirected to the index page,
            # thus a status code of 302 is returned.
            self.assertEqual(response.status_code, http_status.HTTP_302_FOUND)
            # login and test again

    def test_categories_list(self):
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
