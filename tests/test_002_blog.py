import unittest

from pytistory import PyTistory

class TestBlog(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

    def test001_블로그_정보_받아오기(self):
        data = self.pytistory.blog.info()

        self.assertIn('item', data)

    def tearDown(self):
        pass
