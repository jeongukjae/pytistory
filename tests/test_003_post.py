import unittest

from pytistory import PyTistory
from pytistory.exceptions import NoSpecifiedBlogError, ParsingError

class TestPost(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

    def test001_최근_게시글_목록(self):
        data = self.pytistory.post.list(blog_name='test-blog-5532')
        self.assertEqual('1', data['item']['page'])

    def test002_최근_게시글_목록_블로그_비_명시(self):
        self.assertRaises(NoSpecifiedBlogError, self.pytistory.post.list)

    def test003_블로그_없을_때(self):
        self.assertRaises(ParsingError, self.pytistory.post.list,\
            blog_name='test-blog-5555-not-found')

    def test004_블로그_글_작성(self):
        response = self.pytistory.post.write('테스트 포스팅', blog_name='test-blog-5532',\
            visibility=2, content='글 내용', tag=['가나다', '라마바'])
        post_id = response['postId']

        post_response = self.pytistory.post.read(post_id, blog_name='test-blog-5532')
        self.assertIn('글 내용', post_response['item']['content'])
        self.assertIn('테스트 포스팅', post_response['item']['title'])
        self.assertIn('가나다', post_response['item']['tags']['tag'])

    def tearDown(self):
        pass
