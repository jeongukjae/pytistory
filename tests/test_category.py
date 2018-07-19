# -*- coding:utf8 -*-
import os
import warnings
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
                            }
                        ]
                    }
                }
            }
        })
        self.pytistory.category.list(blog_name='test-blog-5532')

    @requests_mock.mock()
    def test_카테고리_목록_target_url_deprecated(self, mock):
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
                            }
                        ]
                    }
                }
            }
        })
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.pytistory.category.list(target_url='http://oauth.tistory.com')

            assert len(w) == 1
            assert "A parameter `targetUrl` is deprecated." in str(
                w[-1].message)
