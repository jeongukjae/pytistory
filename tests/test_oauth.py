# -*- coding:utf8 -*-
import time
import unittest
import multiprocessing
import requests
import requests_mock

from pytistory import PyTistory
from pytistory.exceptions import ConfigurationError, TokenNotFoundError, OptionNotFoundError, TokenNotFoundError


class TestOAuth(unittest.TestCase):
    @requests_mock.mock()
    def test_access_token_설정(self, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=302)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=302, headers={
                 'Location': 'some_callback_url/#access_token=some-access-token&state=some-state'})

        pytistory = PyTistory()
        pytistory.configure(client_id='example client id', tistory_id='example tistory id',
                            tistory_password='example tistory password')

        self.assertEqual(pytistory.access_token,
                         'some-access-token', 'Access Token 설정 실패')

    @requests_mock.mock()
    def test_잘못된_CLIENT_ID_와_SECRET_KEY(self, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=400)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=400)

        pytistory = PyTistory()
        self.assertRaises(ConfigurationError,
                          pytistory.configure,
                          client_id='example client id',
                          tistory_id='example tistory id',
                          tistory_password='example tistory password')

    @requests_mock.mock()
    def test_잘못된_CLIENT_ID_와_SECRET_KEY_2(self, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=302)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=400)

        pytistory = PyTistory()
        self.assertRaises(ConfigurationError,
                          pytistory.configure,
                          client_id='example client id',
                          tistory_id='example tistory id',
                          tistory_password='example tistory password')

    @requests_mock.mock()
    def test_access_token을_찾을_수_없을_때(self, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=302)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=302)

        pytistory = PyTistory()
        self.assertRaises(ConfigurationError,
                          pytistory.configure,
                          client_id='example client id',
                          tistory_id='example tistory id',
                          tistory_password='example tistory password')

    @requests_mock.mock()
    def test_access_token을_찾을_수_없을_때_2(self, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=302)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=302, headers={
                 'Location': 'some_callback_url/#state=some-state'})

        pytistory = PyTistory()
        self.assertRaises(ConfigurationError,
                          pytistory.configure,
                          client_id='example client id',
                          tistory_id='example tistory id',
                          tistory_password='example tistory password')

    def test_토큰이_설정되지_않았을_때(self):
        pytistory = PyTistory()
        self.assertRaises(TokenNotFoundError, pytistory.blog.info)

    def test_아무런_설정_옵션이_없을_때(self):
        pytistory = PyTistory()
        self.assertRaises(OptionNotFoundError, pytistory.configure)

    def test_callback_server를_이용한_인증(self):
        process = multiprocessing.Process(target=send_access_token)
        process.start()

        pytistory = PyTistory()
        pytistory.__TESTING__ = True
        pytistory.configure(client_id='some-client-id')

        process.join()

        self.assertEqual(pytistory.access_token,
                         'some-access-token', 'Access Token 설정 실패')

    def test_callback_server를_이용한_인증_에러(self):
        process = multiprocessing.Process(target=send_access_token_error)
        process.start()

        pytistory = PyTistory()
        pytistory.__TESTING__ = True
        self.assertRaises(TokenNotFoundError,
                          pytistory.configure, client_id='some-client-id')

        process.join()


def send_access_token():
    while not PyTistory._is_listening():
        time.sleep(0.1)

    resp = requests.get(
        'http://0.0.0.0:5000/callback_modified?access_token=some-access-token&state=some-state')

    return resp


def send_access_token_error():
    while not PyTistory._is_listening():
        time.sleep(0.1)

    resp = requests.get(
        'http://0.0.0.0:5000/callback_modified?access_token=&state=some-state')

    return resp
