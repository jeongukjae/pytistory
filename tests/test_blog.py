# -*- coding:utf8 -*-
import unittest
import requests_mock

from pytistory import PyTistory


class TestBlog(unittest.TestCase):
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
    def test_블로그_정보_받아오기(self, mock):
        mock.get('https://www.tistory.com/apis/blog/info', json={
            "tistory": {
                "status": "200",
                "id": "blogtest_080@hanmail.net",
                "item": [
                    {
                        "url": "http://oauth.tistory.com",
                        "secondaryUrl": "http://",
                        "nickname": "Tistory API",
                        "title": "나만의 앱, Tistory OAuth API 로 만들어보세요!",
                        "description": "",
                        "default": "Y",
                        "blogIconUrl": "http://i1.daumcdn.net/cfs.tistory/blog/79/795307/index.gif",
                        "faviconUrl": "http://i1.daumcdn.net/cfs.tistory/blog/79/795307/index.ico",
                        "profileThumbnailImageUrl": "http://cfile1.uf.tistory.com/R106x0/1851DB584DAF942950AF29",
                        "profileImageUrl": "http://cfile1.uf.tistory.com/R106x0/1851DB584DAF942950AF29",
                        "statistics": {
                            "post": "3",
                            "comment": "0",
                            "trackback": "0",
                            "guestbook": "0",
                            "invitation": "0"
                        }
                    },
                    {
                        "url": "http://oauth2.tistory.com",
                        "secondaryUrl": "http://",
                        "nickname": "Tistory API",
                        "title": "나만의 비밀 홈",
                        "description": "",
                        "default": "N",
                        "blogIconUrl": "http://i1.daumcdn.net/cfs.tistory/blog/79/795308/index.gif",
                        "faviconUrl": "http://i1.daumcdn.net/cfs.tistory/blog/79/795308/index.ico",
                        "profileThumbnailImageUrl": "",
                        "profileImageUrl": "",
                        "blogId": "795308",
                        "statistics": {
                            "post": "0",
                            "comment": "0",
                            "trackback": "0",
                            "guestbook": "0",
                            "invitation": "0"
                        }
                    }
                ]
            }
        })

        data = self.pytistory.blog.info()
        self.assertIn('item', data)
