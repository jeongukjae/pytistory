import unittest

from pytistory import PyTistory

class TestOAuth(unittest.TestCase):
    def setUp(self):
        pass

    def test001_설정(self):
        pytistory = PyTistory()
        pytistory.configure()

    def tearDown(self):
        pass
