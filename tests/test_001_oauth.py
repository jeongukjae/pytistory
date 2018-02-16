# -*- coding:utf8 -*-
import unittest

from pytistory import PyTistory
from pytistory.exceptions import ConfigurationError

class TestOAuth(unittest.TestCase):
    def setUp(self):
        pass

    def test001_설정(self):
        pytistory = PyTistory()
        pytistory.configure()

    def test002_잘못된_CLIENT_ID_와_SECRET_KEY(self):
        pytistory = PyTistory()
        self.assertRaises(ConfigurationError, pytistory.configure, client_id='asdf', \
            secret_key='asdf', tistory_id='asdf', tistory_password='asdf')

    def tearDown(self):
        pass
