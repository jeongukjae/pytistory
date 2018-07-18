# -*- coding: utf8 -*-
import unittest
import requests_mock

from pytistory import PyTistory


class TestComment(unittest.TestCase):
    @requests_mock.mock()
    def setUp(self, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=302)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=302, headers={
                 'Location': 'some_callback_url/#access_token=some-access-token&state=some-state'})

        self.pytistory = PyTistory()
        self.pytistory.configure(client_id='example client id',
                                 tistory_id='example tistory id',
                                 tistory_password='example tistory password')

    @requests_mock.mock()
    def test_댓글_리스트_받아오기(self, mock):
        mock.get('https://www.tistory.com/apis/comment/list', json={
            "tistory": {
                "status": "200",
                "item": {
                    "url": "http://oauth.tistory.com/4",
                    "secondaryUrl": "",
                    "postId": "4",
                    "totalCount": "3",
                    "comments": {
                        "comment": [
                            {
                                "id": "8176918",
                                "date": "1303796711",
                                "name": "지나다가",
                                "parentId": "",
                                "homepage": "http://someurl.com",
                                "visibility": "2",
                                "comment": "좋은 글 감사합니다.",
                                "open": "Y"
                            }
                        ]
                    }
                }
            }
        })
        self.pytistory.comment.list(1, blog_name='test')

    @requests_mock.mock()
    def test_최근_댓글_목록_가져오기(self, mock):
        mock.get('https://www.tistory.com/apis/comment/newest', json={
            "tistory": {
                "status": "200",
                "item": {
                    "url": "http://oauth.tistory.com",
                    "secondaryUrl": "",
                    "comments": {
                        "comment": [
                            {
                                "id": "8176926",
                                "date": "1303796900",
                                "postId": "4",
                                "name": "Tistory API",
                                "homepage": "http://oauth.tistory.com",
                                "comment": "비루한 글에 칭찬을 하시니 몸둘바를 모르.. 지 않아!",
                                "open": "Y",
                                "link": "http://oauth.tistory.com/4#comment8176926"
                            }
                        ]
                    }
                }
            }
        })
        self.pytistory.comment.newest(blog_name='test')

    @requests_mock.mock()
    def test_댓글_작성하기(self, mock):
        mock.post('https://www.tistory.com/apis/comment/write', json={
            "tistory": {
                "status": "200",
                "commentUrl": "http://oauth.tistory.com/4#comment8176976",
                "result": "OK"
            }
        })
        resp = self.pytistory.comment.write(1, '댓글-예시', blog_name='test')
        self.assertEqual(resp['result'], 'OK', '댓글을 작성할 수 없습니다.')
        resp = self.pytistory.comment.write(
            2, '댓글-예시', blog_name='test', parent_id=1)
        self.assertEqual(resp['result'], 'OK', '댓글을 작성할 수 없습니다.')
        resp = self.pytistory.comment.write(
            1, '댓글-예시', blog_name='test', secret=1)
        self.assertEqual(resp['result'], 'OK', '댓글을 작성할 수 없습니다.')

    @requests_mock.mock()
    def test_댓글_수정하기(self, mock):
        mock.post('https://www.tistory.com/apis/comment/modify', json={
            "tistory": {
                "status": "200",
                "commentUrl": "http://oauth.tistory.com/4#comment8176976",
                "result": "OK"
            }
        })
        resp = self.pytistory.comment.modify(1, 1, '수정된 댓글', blog_name='test')
        self.assertEqual(resp['result'], 'OK', '댓글을 작성할 수 없습니다.')
        resp = self.pytistory.comment.modify(
            1, 1, '수정된 댓글', blog_name='test', parent_id=1)
        self.assertEqual(resp['result'], 'OK', '댓글을 작성할 수 없습니다.')
        resp = self.pytistory.comment.modify(
            1, 1, '수정된 댓글', blog_name='test', secret=1)
        self.assertEqual(resp['result'], 'OK', '댓글을 작성할 수 없습니다.')

    @requests_mock.mock()
    def test_댓글_삭제하기(self, mock):
        mock.post('https://www.tistory.com/apis/comment/delete', json={
            "tistory": {
                "status": "200"
            }
        })
        self.pytistory.comment.delete(1, 1, blog_name='test')
