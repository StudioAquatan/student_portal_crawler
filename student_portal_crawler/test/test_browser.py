import contextlib
from unittest import TestCase
from unittest.mock import MagicMock, patch
from nose.tools import ok_, eq_

from student_portal_crawler.browser import PortalBrowser
from student_portal_crawler.page import Page
from student_portal_crawler.parser import SupportedPages


class TestPortalBrowser(TestCase):
    """Test case for `browser.PortalBrowser`"""

    def setUp(self):
        self.sample_url = 'https://www.example.com/'
        self.sample_response = MagicMock(
            text='',
            status_code=200,
            url='https://www.example.com/'
        )
        self.sample_parser = MagicMock(
            return_value=MagicMock(
                data={'data': ''},
                soup=''
            )
        )
        self.test_user = 'test'
        self.test_password = 'pass'

    def test_registered_page(self):
        """Get registered page test for `browser.PortalBrowser`"""
        with contextlib.ExitStack() as stack:
            stack.enter_context(
                patch.dict('student_portal_crawler.parser.REGISTERED_PARSERS', {self.sample_url: self.sample_parser})
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

    def test_get_lec_info(self):
        """Get lecture information test for `browser.PortalBrowser`"""
        url = SupportedPages.LECTURE_INFORMATION.value
        with contextlib.ExitStack() as stack:
            patched_get = stack.enter_context(
                patch('student_portal_crawler.shibboleth_login.ShibbolethClient.get', return_value=self.sample_response)
            )
            stack.enter_context(
                patch.dict('student_portal_crawler.parser.REGISTERED_PARSERS', {url: self.sample_parser})
            )
            with PortalBrowser(self.test_user, self.test_password) as b:
                page = b.get_lecture_information()
                ok_(patched_get.called)
                ok_(patched_get.call_count, 1)
                positional_args = patched_get.call_args[0]
                eq_(positional_args[0], url)
                eq_(type(page), Page)
                eq_(page.status_code, self.sample_response.status_code)
                eq_(page.url, self.sample_url)
                eq_(page.html, self.sample_response.text)
                eq_(page.as_dict, self.sample_parser().data)
