from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from nose.tools import eq_

from student_portal_crawler.page import Page


class TestPage(TestCase):
    """Test case for `base.Page`"""

    @classmethod
    def setUpClass(cls):
        cls.sample_date = datetime.strptime('2018/3/31', '%Y/%m/%d')
        cls.sample_response = MagicMock(
            text='',
            status_code=200,
            url='https://www.example.com/'
        )
        cls.sample_parser = MagicMock(
            return_value=MagicMock(
                data={'data': ''},
                soup='soup'
            )
        )

    def test_check_params(self):
        """Parameters validation test fo `base.Page`"""
        page = Page(self.sample_response, self.sample_parser, self.sample_date)
        eq_(page.url, self.sample_response.url)
        eq_(page.html, self.sample_response.text)
        eq_(page.status_code, self.sample_response.status_code)
        eq_(page.as_dict, self.sample_parser().data)
        eq_(page.soup, self.sample_parser().soup)
        eq_(page.access_at, self.sample_date)
