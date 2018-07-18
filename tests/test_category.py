# -*- coding:utf8 -*-
import os
import unittest
import requests_mock

from pytistory import PyTistory


class TestCategory(unittest.TestCase):
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
    def test_카테고리_목록(self, mock):
        mock.get('https://www.tistory.com/apis/category/list', json={
            "tistory": {
                "status": "200",
                "item": {
                    "url": "oauth",
                    "secondaryUrl": "",
                    "categories": {
                        "category": [
                            {
                                "id": "403929",
                                "name": "OAuth2.0 Athentication",
                                "parent": "",
                                "label": "OAuth2.0 Athentication",
                                "entries": "0"
                            },
                            {
                                "id": "403930",
                                "name": "Blog API Series",
                                "parent": "",
                                "label": "Blog API Series",
                                "entries": "0"
                            },
                            {
                                "id": "403931",
                                "name": "Post API Series",
                                "parent": "",
                                "label": "Post API Series",
                                "entries": "0"
                            },
                            {
                                "id": "403932",
                                "name": "Category API Series",
                                "parent": "",
                                "label": "Category API Series",
                                "entries": "0"
                            },
                            {
                                "id": "403933",
                                "name": "Comment API Series",
                                "parent": "",
                                "label": "Comment API Series",
                                "entries": "0"
                            },
                            {
                                "id": "403934",
                                "name": "Guestbook API Series",
                                "parent": "",
                                "label": "Guestbook API Series",
                                "entries": "0"
                            }
                        ]
                    }
                }
            }
        })
        self.pytistory.category.list(blog_name='test-blog-5532')

    def tearDown(self):
        pass
