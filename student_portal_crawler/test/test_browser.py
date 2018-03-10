import contextlib
from unittest import TestCase
from unittest.mock import MagicMock, patch
from nose.tools import ok_, eq_

from student_portal_crawler.browser import PortalBrowser
from student_portal_crawler.page import Page


class TestPortalBrowser(TestCase):
    """Test case for `browser.PortalBrowser`"""

    @classmethod
    def setUpClass(cls):
        cls.sample_url = 'https://www.example.com/'
        cls.sample_response = MagicMock(
            text='',
            status_code=200,
            url='https://www.example.com/'
        )
        cls.sample_parser = MagicMock(
            return_value=MagicMock(
                data={'data': ''},
                soup=''
            )
        )
        cls.patched_registered_dict = {
            cls.sample_url: cls.sample_parser
        }
        cls.test_user = 'test'
        cls.test_password = 'pass'

    def test_registered_page(self):
        """Get registered page test for `browser.PortalBrowser`"""
        with contextlib.ExitStack() as stack:
            stack.enter_context(
                patch.dict('student_portal_crawler.parser.REGISTERED_PARSERS', self.patched_registered_dict)
            )
            patched_get = stack.enter_context(
                patch('student_portal_crawler.shibboleth_login.ShibbolethClient.get', return_value=self.sample_response)
            )
            with PortalBrowser(self.test_user, self.test_password) as b:
                page = b.get_page(self.sample_url)
                ok_(patched_get.called)
                ok_(patched_get.call_count, 1)
                positional_args = patched_get.call_args[0]
                eq_(positional_args[0], self.sample_url)
                eq_(type(page), Page)
                eq_(page.status_code, self.sample_response.status_code)
                eq_(page.url, self.sample_url)
                eq_(page.html, self.sample_response.text)
                eq_(page.as_dict, self.sample_parser().data)
                eq_(page.soup, self.sample_parser().soup)

    def test_unregistered_page(self):
        """Get unregistered page test for `browser.PortalBrowser`"""
        with contextlib.ExitStack() as stack:
            patched_get = stack.enter_context(
                patch('student_portal_crawler.shibboleth_login.ShibbolethClient.get', return_value=self.sample_response)
            )
            patched_parser = stack.enter_context(
                patch('student_portal_crawler.parser.GeneralParser', self.sample_parser)
            )
            with PortalBrowser(self.test_user, self.test_password) as b:
                page = b.get_page(self.sample_url)
                ok_(patched_get.called)
                ok_(patched_get.call_count, 1)
                positional_args = patched_get.call_args[0]
                eq_(positional_args[0], self.sample_url)
                eq_(type(page), Page)
                eq_(page.status_code, self.sample_response.status_code)
                eq_(page.url, self.sample_url)
                eq_(page.html, self.sample_response.text)
                eq_(page.as_dict, self.sample_parser().data)
                ok_(patched_parser.called)
                ok_(patched_get.call_count, 1)
