# -*- coding:utf8 -*-
import os
import unittest

from selenium import webdriver

from pytistory import PyTistory
from pytistory.exceptions import NoSpecifiedBlogError, ParsingError

class TestCategory(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

    def test001_최근_게시글_목록(self):
        self.pytistory.category.list()

    def tearDown(self):
        pass
