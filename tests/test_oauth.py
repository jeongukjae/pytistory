# -*- coding:utf8 -*-
import time
import unittest
import unittest.mock
import multiprocessing
import requests
import requests_mock

from pytistory import PyTistory
from pytistory.exceptions import (ConfigurationError, TokenNotFoundError,
                                  OptionNotFoundError, TokenNotFoundError, InvalidSectionError, InvalidNameError)

TEST_FILE_CLIENT_ID = """
[pytistory]
client_id=some-test-client-id
"""
TEST_FILE_FULL = """
[pytistory]
client_id=some-test-client-id
tistory_id=some-tistory-id
tistory_password=some-tistory-password
"""


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
        while PyTistory._is_listening():
            time.sleep(0.1)

        process = multiprocessing.Process(target=send_access_token)
        process.start()

        pytistory = PyTistory()
        pytistory.__TESTING__ = True
        pytistory.configure(client_id='some-client-id')

        self.assertEqual(pytistory.access_token,
                         'some-access-token', 'Access Token 설정 실패')

        process.join()

    def test_callback_server를_이용한_인증_에러(self):
        while PyTistory._is_listening():
            time.sleep(0.1)

        process = multiprocessing.Process(target=send_access_token_error)
        process.start()

        pytistory = PyTistory()
        pytistory.__TESTING__ = True
        self.assertRaises(TokenNotFoundError,
                          pytistory.configure, client_id='some-client-id')

        process.join()

    @unittest.mock.patch("os.path.isfile", return_value=True)
    @unittest.mock.patch("os.path.exists", return_value=True)
    @unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=TEST_FILE_FULL))
    @requests_mock.mock()
    def test_파일을_통한_인증(self, _1, _2, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=302)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=302, headers={
                 'Location': 'some_callback_url/#access_token=some-access-token&state=some-state'})

        pytistory = PyTistory()
        pytistory.configure()

        self.assertEqual(pytistory.access_token,
                         'some-access-token', 'Access Token 설정 실패')

    @unittest.mock.patch("os.path.isfile", return_value=True)
    @unittest.mock.patch("os.path.exists", return_value=True)
    @unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=TEST_FILE_FULL))
    @requests_mock.mock()
    def test_파일을_통한_인증_파일명_넘길_때(self, _1, _2, mock):
        mock.post('https://www.tistory.com/auth/login', status_code=302)
        mock.get('https://www.tistory.com/oauth/authorize', status_code=302, headers={
                 'Location': 'some_callback_url/#access_token=some-access-token&state=some-state'})

        pytistory = PyTistory()
        pytistory.configure(file_name='some-file-name')

        self.assertEqual(pytistory.access_token,
                         'some-access-token', 'Access Token 설정 실패')

    @unittest.mock.patch("os.path.isfile", return_value=True)
    @unittest.mock.patch("os.path.exists", return_value=True)
    @unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=TEST_FILE_CLIENT_ID))
    def test_파일을_통한_인증_CLIENT_ID만(self, _1, _2):
        while PyTistory._is_listening():
            time.sleep(0.1)

        process = multiprocessing.Process(target=send_access_token)
        process.start()

        pytistory = PyTistory()
        pytistory.__TESTING__ = True
        pytistory.configure()

        self.assertEqual(pytistory.access_token,
                         'some-access-token', 'Access Token 설정 실패')

        process.join()

    @unittest.mock.patch("os.path.isfile", return_value=True)
    @unittest.mock.patch("os.path.exists", return_value=False)
    def test_파일을_통한_인증_오류(self, _1, _2):
        pytistory = PyTistory()
        pytistory.__TESTING__ = True

        self.assertRaises(ConfigurationError, pytistory.configure,
                          file_name='')
        self.assertRaises(ConfigurationError, pytistory.configure,
                          file_name='asdf')

        _1.return_value = True
        with unittest.mock.patch(
            'builtins.open',
                unittest.mock.mock_open(read_data="")):
            self.assertRaises(InvalidSectionError,
                              pytistory.configure,
                              file_name='asdf')

        with unittest.mock.patch(
            'builtins.open',
                unittest.mock.mock_open(read_data="[pytistory]")):
            self.assertRaises(InvalidNameError,
                              pytistory.configure,
                              file_name='asdf')


def send_access_token():
    while not PyTistory._is_listening():
        time.sleep(0.1)

    resp = requests.get(
        'http://0.0.0.0:5000/callback#access_token=some-access-token&state=some-state')

    resp = requests.get(
        'http://0.0.0.0:5000/callback_modified?access_token=some-access-token&state=some-state')

    return resp


def send_access_token_error():
    while not PyTistory._is_listening():
        time.sleep(0.1)

    resp = requests.get(
        'http://0.0.0.0:5000/callback#access_token=some-access-token&state=some-state')

    resp = requests.get(
        'http://0.0.0.0:5000/callback_modified?access_token=&state=some-state')

    return resp
