from unittest import TestCase
import requests

class TestReachable(TestCase):

    def test_system1_domain1_is_reachable(self):
        self.assertReachable('http://system1.domain1.com')
    
    def test_system2_domain1_is_reachable(self):
        self.assertReachable('http://system2.domain1.com')

    def test_system1_domain2_is_reachable(self):
        self.assertReachable('http://system1.domain2.com')
    
    def test_system2_domain2_is_reachable(self):
        self.assertReachable('http://system2.domain2.com')


    def assertReachable(self, url):
        try:
            code = requests.get(url, timeout=0.5).status_code
            self.assertEqual(200, code)
        except requests.exceptions.ReadTimeout:
            self.fail(f'{url} is not reachable. Timout')
        except  requests.exceptions.ConnectionError:
            self.fail(f'{url} is not reachable. Connection Error')
        