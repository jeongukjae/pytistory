# -*- coding:utf8 -*-
import os
import unittest
import datetime
import requests_mock

from pytistory import PyTistory
from pytistory.exceptions import NoSpecifiedBlogError, ParsingError


class TestPost(unittest.TestCase):
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
    def test_최근_게시글_목록(self, mock):
        mock.get('https://www.tistory.com/apis/post/list', json={
            "tistory": {
                "status": "200",
                "item": {
                    "url": "http://oauth.tistory.com",
                    "secondaryUrl": "",
                    "page": "1",
                    "count": "10",
                    "totalCount": "4",
                    "posts": {
                        "post": [
                            {
                                "id": "4",
                                "title": "티스토리 OAuth Open API 일단 써보세요!",
                                "postUrl": "http://oauth.tistory.com /4",
                                "visibility": "0",
                                "categoryId": "0",
                                "comments": "6",
                                "trackbacks": "0",
                                "date": "1303796661"
                            },
                            {
                                "id": "3",
                                "title": "View에 보냅니다~",
                                "postUrl": "http://oauth.tistory.com /3",
                                "visibility": "3",
                                "categoryId": "0",
                                "comments": "0",
                                "trackbacks": "0",
                                "date": "1303372106"
                            },
                            {
                                "id": "2",
                                "title": "View에 보내봅니다.",
                                "postUrl": "http://oauth.tistory.com /2",
                                "visibility": "3",
                                "categoryId": "0",
                                "comments": "0",
                                "trackbacks": "0",
                                "date": "1303372007"
                            },
                            {
                                "id": "1",
                                "title": "티스토리 OAuth2.0 API 오픈!",
                                "postUrl": "http://oauth.tistory.com /1",
                                "visibility": "0",
                                "categoryId": "0",
                                "comments": "0",
                                "trackbacks": "0",
                                "date": "1303352668"
                            }
                        ]
                    }
                }
            }
        })
        data = self.pytistory.post.list(blog_name='oauth')
        self.assertEqual('1', data['item']['page'])

    def test_최근_게시글_목록_블로그_비_명시(self):
        self.assertRaises(NoSpecifiedBlogError, self.pytistory.post.list)

    @requests_mock.mock()
    def test_블로그_없을_때(self, mock):
        mock.get('https://www.tistory.com/apis/post/list', json={
            "tistory": {
                "status": "400",
                "item": {}
            }
        })

        self.assertRaises(ParsingError, self.pytistory.post.list,
                          blog_name='oauth-not-found')

    @requests_mock.mock()
    def test_블로그_글_작성(self, mock):
        mock.post('https://www.tistory.com/apis/post/write', json={
            "tistory": {
                "status": "200",
                "postId": "1",
                "url": "http://sampleUrl.tistory.com/1"
            }
        })
        response = self.pytistory.post.write('테스트 포스팅',
                                             blog_name='oauth',
                                             visibility=2,
                                             content='글 내용',
                                             tag=['가나다', '라마바'])
        self.assertEqual(response['postId'], "1", "포스팅 작성 불가")

        response = self.pytistory.post.write('테스트 포스팅',
                                             blog_name='oauth',
                                             visibility=2,
                                             content='글 내용',
                                             published=datetime.datetime.now())
        self.assertEqual(response['postId'], "1", "포스팅 작성 불가")

    def test_블로그_글_작성_에러(self):
        self.assertRaises(TypeError,
                          self.pytistory.post.write,
                          '테스트 포스팅',
                          blog_name='oauth',
                          visibility='a',
                          content='글 내용',
                          tag=['가나다', '라마바'])

        self.assertRaises(TypeError,
                          self.pytistory.post.write,
                          '테스트 포스팅',
                          blog_name='oauth',
                          visibility=2,
                          published='b',
                          content='글 내용',
                          tag=['가나다', '라마바'])

        self.assertRaises(TypeError,
                          self.pytistory.post.write,
                          '테스트 포스팅',
                          blog_name='oauth',
                          visibility=2,
                          content='글 내용',
                          published=datetime.datetime.now(),
                          tag='가나다')

    @requests_mock.mock()
    def test_블로그_글_읽기(self, mock):
        mock.get('https://www.tistory.com/apis/post/read', json={
            "tistory": {
                "status": "200",
                "item": {
                    "url": "http://oauth.tistory.com",
                    "secondaryUrl": "",
                    "id": "1",
                    "title": "티스토리 OAuth2.0 API 오픈!",
                    "content": "안녕하세요 Tistory API 입니다.<br><br>이번에 Third-party Developer 용 <b>Tistory OAuth 2.0 API</b> 가 오픈됩니다.<br>Tistory 회원이라면, 여러분의 모든 app에 자유롭게 활용하실 수 있습니다. 많은 기대와 사랑 부탁드립니다. < br > ",
                    "categoryId": "0",
                    "postUrl": "http://oauth.tistory.com/1",
                    "visibility": "0",
                    "acceptComment": "1",
                    "acceptTrackback": "1",
                    "tags": {
                        "tag": ["open", "api"]
                    },
                    "comments": "0",
                    "trackbacks": "0",
                    "date": "1303352668"
                }
            }
        })
        post_response = self.pytistory.post.read(12, blog_name='oauth')

        self.assertIn('안녕하세요 Tistory API 입니다.',
                      post_response['item']['content'])
        self.assertIn('티스토리 OAuth2.0 API 오픈!', post_response['item']['title'])
        self.assertIn('open', post_response['item']['tags']['tag'])

    @requests_mock.mock()
    def test_블로그_글_수정(self, mock):
        mock.post('https://www.tistory.com/apis/post/modify', json={
            "tistory": {
                "status": "200",
                "postId": "1",
                "url": "http://sampleUrl.tistory.com/1"
            }
        })

        response = self.pytistory.post.modify('테스트 포스팅 - 수정',
                                              1,
                                              blog_name='oauth',
                                              visibility=2,
                                              content='글 내용 - 수정',
                                              tag=['가나다', '라마바', '수정'])

        self.assertEqual(response['postId'], "1", "수정 불가")

        response = self.pytistory.post.modify('테스트 포스팅 - 수정',
                                              1,
                                              blog_name='oauth',
                                              visibility=2,
                                              content='글 내용 - 수정')

        self.assertEqual(response['postId'], "1", "수정 불가")

    def test_블로그_글_수정_에러(self):
        self.assertRaises(TypeError,
                          self.pytistory.post.modify,
                          '테스트 포스팅',
                          1,
                          blog_name='oauth',
                          visibility='a',
                          content='글 내용',
                          tag=['가나다', '라마바'])

        self.assertRaises(TypeError,
                          self.pytistory.post.modify,
                          '테스트 포스팅',
                          1,
                          blog_name='oauth',
                          visibility=2,
                          content='글 내용',
                          tag='가나다')

    @requests_mock.mock()
    def test_파일_첨부_후_게시(self, mock):
        mock.post('https://www.tistory.com/apis/post/attach', json={
            "tistory": {
                "status": "200",
                "url": "http://cfile6.uf.tistory.com/image/1328CE504DB79F5932B13F",
                "replacer": "%5b%23%23_1N%7ccfile6.uf%401328CE504DB79F5932B13F%7cwidth%3d\"500\"+height%3d\"300\"%7c_%23%23%5d"
            }
        })
        self.pytistory.post.attach('tests/test_image.png', blog_name='oauth')

    def test_파일_첨부_후_게시_파일_읽기_오류(self):
        self.assertRaises(FileNotFoundError,
                          self.pytistory.post.attach,
                          'tests/test_image_not-found.png',
                          blog_name='oauth')

    @requests_mock.mock()
    def test_블로그_글_삭제(self, mock):
        mock.post('https://www.tistory.com/apis/post/delete', json={
            "tistory": {
                "status": "200"
            }
        })
        self.pytistory.post.delete(1, blog_name='oauth')
