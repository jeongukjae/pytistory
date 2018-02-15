import unittest

from pytistory import PyTistory

class TestPost(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

    def test001_최근_게시글_목록(self):
        data = self.pytistory.post.list(blog_name='test-blog-5532')
        self.assertEqual('1', data['item']['page'])

    def tearDown(self):
        pass
