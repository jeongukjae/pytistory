# -*- coding: utf8 -*-
import unittest
import requests_mock

from pytistory import PyTistory


class TestGuestbook(unittest.TestCase):
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
    def test_방명록_리스트_받아오기(self, mock):
        mock.get('https://www.tistory.com/apis/guestbook/list', json={
            "tistory": {
                "status": "200",
                "item": {
                    "url": "http://oauth.tistory.com",
                    "secondaryUrl": "",
                    "page": "1",
                    "totalCount": "2",
                    "guestbooks": {
                        "guestbook": [
                            {
                                "id": "8177011",
                                "date": "1303798898",
                                "name": "잘못들어온 사람",
                                "homepage": "http://wrongway.com",
                                "comment": "아.. 저 여기 잘못들어왔나봐요..",
                                "open": "Y",
                                "replies": {
                                    "reply": {
                                        "id": "8177015",
                                        "date": "1303799030",
                                        "name": "Tistory API",
                                        "parentId": "8177011",
                                        "homepage": "http://oauth.tistory.com",
                                        "comment": "들어올때는 마음대로 들어왔겠지만 나갈때는 아니란다",
                                        "open": "Y"
                                    }
                                }
                            },
                            {
                                "id": "8177008",
                                "date": "1303798795",
                                "name": "개발자",
                                "homepage": "http://somedeveloper.com",
                                "comment": "좋은 API 많이 만들어주세요!",
                                "open": "Y",
                                "replies": ""
                            }
                        ]
                    }
                }
            }
        })
        self.pytistory.guestbook.list(blog_name='test')

    @requests_mock.mock()
    def test_방명록_작성(self, mock):
        mock.post('https://www.tistory.com/apis/guestbook/write', json={
            "tistory": {
                "status": "200",
                "guestbookUrl": "http://oauth.tistory.com/guestbook",
                "result": "OK"
            }
        })
        self.pytistory.guestbook.write('방명록 내용', blog_name='test')
        self.pytistory.guestbook.write('방명록 내용', blog_name='test', parent_id=1)
        self.pytistory.guestbook.write('방명록 내용', blog_name='test', secret=1)

    @requests_mock.mock()
    def test_방명록_수정(self, mock):
        mock.post('https://www.tistory.com/apis/guestbook/modify', json={
            "tistory": {
                "status": "200",
                "guestbookUrl": "http://oauth.tistory.com/guestbook",
                "result": "OK"
            }
        })
        self.pytistory.guestbook.modify(1, '수정된 방명록 내용', blog_name='test')
        self.pytistory.guestbook.modify(
            1, '수정된 방명록 내용', blog_name='test', parent_id=1)
        self.pytistory.guestbook.modify(
            1, '수정된 방명록 내용', blog_name='test', secret=1)

    @requests_mock.mock()
    def test_방명록_삭제(self, mock):
        mock.post('https://www.tistory.com/apis/guestbook/delete', json={
            "tistory": {
                "status": "200",
            }
        })
        self.pytistory.guestbook.delete(1, blog_name='test')
