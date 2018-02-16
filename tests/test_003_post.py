import unittest

from pytistory import PyTistory
from pytistory.exceptions import NoSpecifiedBlogError

class TestPost(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

    def test001_최근_게시글_목록(self):
        data = self.pytistory.post.list(blog_name='test-blog-5532')
        self.assertEqual('1', data['item']['page'])

    def test002_최근_게시글_목록_블로그_비_명시(self):
        self.assertRaises(NoSpecifiedBlogError, self.pytistory.post.list)

    def tearDown(self):
        pass
