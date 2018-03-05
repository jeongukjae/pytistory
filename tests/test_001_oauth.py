# -*- coding:utf8 -*-
import unittest

from pytistory import PyTistory
from pytistory.exceptions import ConfigurationError, TokenNotFoundError

class TestOAuth(unittest.TestCase):
    def setUp(self):
        pass

    def test001_설정(self):
        pytistory = PyTistory()
        pytistory.configure()

    def test002_잘못된_CLIENT_ID_와_SECRET_KEY(self):
        pytistory = PyTistory()
        self.assertRaises(ConfigurationError, pytistory.configure, client_id='asdf', \
            tistory_id='asdf', tistory_password='asdf')

    def test003_토큰이_설정되지_않았을_때(self):
        pytistory = PyTistory()
        self.assertRaises(TokenNotFoundError, pytistory.blog.info)

    def tearDown(self):
        pass
