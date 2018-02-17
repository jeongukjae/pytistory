# -*- coding: utf8 -*-
import unittest

from pytistory import PyTistory

class TestComment(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

    def tearDown(self):
        pass

    def test001_댓글_리스트_받아오기(self):
        self.pytistory.comment.list(1, blog_name='test-blog-5532')
    
    def test002_최근_댓글_목록_가져오기(self):
        self.pytistory.comment.newest(blog_name='test-blog-5532')

    def test003_댓글_작성하기(self):
        data = self.pytistory.comment.write(1, '댓글-예시', blog_name='test-blog-5532')
        comment_id = data['commentUrl'].split('#comment')[1]

        response = self.pytistory.comment.list(1, blog_name='test-blog-5532')

        is_existed = False
        for comment in response['item']['comments']:
            if comment['id'] == comment_id:
                is_existed = True
                break
        
        if not is_existed:
            self.fail('댓글이 작성되지 않음.')

    def test004_댓글_수정하기(self):
        # list_response = self.pytistory.comment.list(1, blog_name='test-blog-5532')
        # comment_id = list_response['item']['comments'][0]['id']

        # modify_response = self.pytistory.comment.modify(1, comment_id, '수정된 댓글', blog_name='test-blog-5532')
        # comment_id = modify_response['commentUrl'].split('#comment')[1]

        # response = self.pytistory.comment.list(1, blog_name='test-blog-5532')
        # for comment in response['item']['comments']:
        #     if comment['id'] == comment_id:
        #         if '수정' not in comment['comment']:
        #             self.fail('수정이 되지 않음')
        #         break
        # 현재 티스토리 블로그 오픈 API 상의 댓글 수정 API로는 댓글이 수정되지 않아요.. ㅜㅜ
        pass

    def test005_댓글_삭제하기(self):
        list_response = self.pytistory.comment.list(1, blog_name='test-blog-5532')
        for comment in list_response['item']['comments']:
            self.pytistory.comment.delete(1, comment['id'], blog_name='test-blog-5532')
        
        list_response = self.pytistory.comment.list(1, blog_name='test-blog-5532')

        if 'comments' in list_response:
            self.fail('삭제에 문제가 있습니다.')
