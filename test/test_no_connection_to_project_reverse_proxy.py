from unittest import TestCase
import requests

class TestNoConnectionToProjectReverseProxies(TestCase):

    def test_system1_domain1_is_reachable(self):
        self.assertNotReachable('http://system1.domain1.com:9001')
    
    def test_system2_domain1_is_reachable(self):
        self.assertNotReachable('http://system2.domain1.com:9001')

    def test_system1_domain2_is_reachable(self):
        self.assertNotReachable('http://system1.domain2.com:9002')
    
    def test_system2_domain2_is_reachable(self):
        self.assertNotReachable('http://system2.domain2.com:9002')


    def assertNotReachable(self, url):
        try:
            requests.get(url, timeout=0.5).status_code
            self.fail(f'{url} should not be reachable, but is')
        except requests.exceptions.ConnectionError:
            pass # happy path
            