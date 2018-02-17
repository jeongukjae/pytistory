# -*- coding: utf8 -*-
import unittest

from pytistory import PyTistory

class TestGuestbook(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

    def tearDown(self):
        pass

    def test001_방명록_리스트_받아오기(self):
        self.pytistory.guestbook.list(blog_name='test-blog-5532')

    def test002_방명록_작성(self):
        self.pytistory.guestbook.write('방명록 내용', blog_name='test-blog-5532')

    def test003_방명록_수정(self):
        list = self.pytistory.guestbook.list(blog_name='test-blog-5532')['item']['guestbooks']
        guestbook_id = list[0]['id']
        self.pytistory.guestbook.modify(guestbook_id, '수정된 방명록 내용', blog_name='test-blog-5532')

        list = self.pytistory.guestbook.list(blog_name='test-blog-5532')['item']['guestbooks']
        for guestbook in list:
            if guestbook['id'] == guestbook_id:
                if '수정' not in guestbook['comment']:
                    self.fail('수정이 되지 않았음.')
                
                break

    def test004_방명록_삭제(self):
        list = self.pytistory.guestbook.list(blog_name='test-blog-5532')['item']['guestbooks']
        guestbook_id = list[0]['id']

        self.pytistory.guestbook.delete(guestbook_id, blog_name='test-blog-5532')
        list = self.pytistory.guestbook.list(blog_name='test-blog-5532')['item']['guestbooks']
        for guestbook in list:
            if guestbook['id'] == guestbook_id:
                self.fail('삭제가 되지 않았음.')
