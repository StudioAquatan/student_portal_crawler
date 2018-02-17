import unittest

from nose.tools import ok_, eq_

from kit_portal_crawler.network import PortalBrowser


class TestPortalBrowser(unittest.TestCase):

    def test_singleton(self):
        instance_a = PortalBrowser("user", "pass")
        instance_b = PortalBrowser("user", "pass")
        eq_(instance_a, instance_b)
        instance_c = PortalBrowser("diff_user", "diff_pass")
        ok_(instance_a != instance_c)
        instance_a.close()
        instance_b.close()
        instance_c.close()

    def test_calc_hash(self):
        hash_a = PortalBrowser._calculate_hash("user", "pass")
        hash_b = PortalBrowser._calculate_hash("user", "pass")
        eq_(hash_a, hash_b)
        hash_c = PortalBrowser._calculate_hash("diff_user", "diff_pass")
        ok_(hash_a != hash_c)
