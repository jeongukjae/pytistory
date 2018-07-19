# -*- coding: utf8 -*-
"""PyTistory를 정의하는 모듈입니다.
"""
import os
import configparser
import multiprocessing
import webbrowser
import time

import requests

from .api import Blog, Category, Post, Comment, Guestbook
from .exceptions import (InvalidSectionError, InvalidNameError, ConfigurationError,
                         OptionNotFoundError, EmailAuthError, WebDriverError, TokenNotFoundError,
                         InvalidAccountError)
from .callback import CallbackServer

TISTORY_AUTHORIZE_URL = 'https://www.tistory.com/oauth/authorize'
TISTORY_AUTHORIZE_PARAMS = '?client_id={0}&redirect_uri=http://0.0.0.0:5000/callback&response_type=token'

CONFIG_SECTION_NAME = 'pytistory'
CONFIG_CLIENT_ID = 'client_id'
CONFIG_TISTORY_ID = 'tistory_id'
CONFIG_TISTORY_PASSWORD = 'tistory_password'

DEFAULT_CONFIG_FILE_NAME = '~/.pytistory/credentials.ini'


def callback_process(namespace, event):
    """flask가 실행되는 process 함수.

    Callback Server를 다른 프로세스로 만들어서 쓰기 위한 함수입니다.
    하나의 프로세스로 동작합니다.

    :param namespace: access_token을 주고 받기 위한 인자
    :type namespace: :class:`multiprocessing.managers.Namespace`
    :param event: 이벤트를 받기 위한 인자
    :type event: :class:`multiprocessing.Event`
    """
    callback = CallbackServer(namespace, event)
    callback.prepare()


class PyTistory:
    """Tistory Api 전체적으로 묶어주는 클래스입니다.

    다음과 같은 기능을 합니다.

      - 인증
    """
    # pylint: disable=too-many-instance-attributes,too-few-public-methods
    # 해당 클래스의 멤버를 통해 api를 부르므로, too-few-public-methods는 체크할 필요가 없다.

    def __init__(self):
        self.__TESTING__ = False

        self.client_id = None
        self.tistory_id = None
        self.tistory_password = None

        self.access_token = None

        self.blog = Blog()
        self.post = Post()
        self.category = Category()
        self.comment = Comment()
        self.guestbook = Guestbook()

    @staticmethod
    def _is_listening():
        try:
            requests.get('http://localhost:5000/')
        except requests.exceptions.ConnectionError:
            return False

        return True

    def _set_access_token(self, headless_auth):
        """Tistory의 access_token을 설정하는 함수입니다.

        `CallbackServer`를 구동시킨 후, 티스토리 인증 창을 브라우저를 통해 엽니다.
        그 후 인증이 되었다면, access_token을 받아옵니다.

        :param headless_auth: Headless 브라우저를 사용해서 인증을 시도할 때 이 인자를 사용합니다.
        :param headless_auth: bool
        :raises EmailAuthError: 티스토리 인증 중 이메일 인증이 필요한 경우입니다.
        :raises TokenNotFoundError: 만약 access_token이 정상적으로 받아와지지 않았을 경우입니다.
        """
        if headless_auth:
            session = requests.Session()
            resp = session.post('https://www.tistory.com/auth/login', data=dict({
                'redirectUrl': 'https://www.tistory.com/oauth/authorize?client_id={}&redirect_uri=http://0.0.0.0:5000/callback&response_type=token'.format(self.client_id),
                'loginId': self.tistory_id,
                'password': self.tistory_password,
                'rememberLoginId': 1
            }), allow_redirects=False)

            if resp.status_code != 302:
                raise ConfigurationError("Cannot Sign into Tistory")

            resp = session.get(
                'https://www.tistory.com/oauth/authorize?client_id={}&redirect_uri=http://0.0.0.0:5000/callback&response_type=token'.format(self.client_id), allow_redirects=False)

            if resp.status_code != 302 or 'Location' not in resp.headers:
                raise ConfigurationError(
                    "Cannot get access token. try configure with browser")

            location = resp.headers['Location']
            params = list(map(lambda x: x.split('='),
                              location.split('#')[1].split('&')))

            for param in params:
                if param[0] == 'access_token':
                    self.access_token = param[1]
                    break

            if self.access_token is None:
                raise ConfigurationError('Cannot get the access_token')

        else:
            multiprocessing_manager = multiprocessing.Manager()
            namespace = multiprocessing_manager.Namespace()
            event = multiprocessing.Event()

            process = multiprocessing.Process(
                target=callback_process, args=(namespace, event))
            process.start()

            if not self.__TESTING__:
                while not self._is_listening():
                    time.sleep(0.1)

                request_uri = TISTORY_AUTHORIZE_URL + \
                    TISTORY_AUTHORIZE_PARAMS.format(self.client_id)
                webbrowser.open_new(request_uri)

            event.wait()
            if hasattr(namespace, 'access_token') and namespace.access_token:  # pylint: disable=E1101
                self.access_token = namespace.access_token  # pylint: disable=E1101
                # disable the pylint message E1101 `Instance of 'Namespace'
                # has no 'access_token' member'`
                # checked in if statement
            else:
                raise TokenNotFoundError('Cannot get the access token from a server. :' +
                                         namespace.error_description if namespace.error_description is not None else 'We can`t find an error.\n please report this as an issue :)\nhttps://github.com/JeongUkJae/pytistory/issues')  # pylint: disable=E1101

            process.join()

    def _configure_with_file(self, file_name, no_error=False):
        """파일을 통한 설정

        :param file_name: 환경 설정파일이 담겨있는 파일 이름, defaults to None
        :type file_name: str, optional
        :param no_error: 에러를 일으키지 않는 옵션 (기본 설정 파일일 때 사용), defaults to False
        :type no_error: bool, optional
        """
        if not file_name:
            raise ConfigurationError("You have to pass a file name")

        if not os.path.exists(file_name) or not os.path.isfile(file_name):
            if no_error:
                return

            raise ConfigurationError(
                "You have to pass the file name that is valid.")

        config = configparser.ConfigParser()
        with open(file_name) as fp:
            config.read_string(fp.read())

            if CONFIG_SECTION_NAME not in config:
                if no_error:
                    return

                raise InvalidSectionError('Cannot find a `{}` section in `{}`.'.
                                          format(CONFIG_SECTION_NAME, file_name))
            if CONFIG_CLIENT_ID not in config[CONFIG_SECTION_NAME]:
                if no_error:
                    return

                raise InvalidNameError('Cannot find a tistory client id in `{}`.'
                                       .format(file_name))

            self.client_id = config[CONFIG_SECTION_NAME][CONFIG_CLIENT_ID]

            # if configuration file includes an account information
            if CONFIG_TISTORY_ID in config[CONFIG_SECTION_NAME]:
                self.tistory_id = config[CONFIG_SECTION_NAME][CONFIG_TISTORY_ID]
            if CONFIG_TISTORY_PASSWORD in config[CONFIG_SECTION_NAME]:
                self.tistory_password = config[CONFIG_SECTION_NAME][CONFIG_TISTORY_PASSWORD]

    # pylint: disable=too-many-arguments
    def configure(self, file_name=None,
                  client_id=None,
                  tistory_id=None,
                  tistory_password=None,
                  force_browser=False,
                  access_token=None):
        """Tistory OAuth 2.0 인증을 실행하는 함수입니다.

        `Tistory Open API OAuth 인증 <http://www.tistory.com/guide/api/oauth>`_ 에
        해당하는 구현이고, Client-side flow방식을 이용하였습니다.
        티스토리 client_id 값을 파일에서 읽거나,
        인자에서 받거나, 환경변수에서 받아서 인증을 하게 됩니다.

        우선순위
         - 함수로 넘어오는 인자값
         - 함수로 넘어오는 파일명에 설정되어 있는 값
         - 환경변수값
         - 기본 파일에 설정되어 있는 값

        만약 file_name도 넘어오고, client_id, tistory_id, tistory_password 중
        하나 이상의 인자가 넘어온다면 file_name에 있던 값들을 인자로 넘긴 값으로 덮어씌운다

        환경 변수의 KEY는 `PYTISTORY_CLIENT_ID` 를
        사용합니다.

        :param file_name: configure 파일 이름, defaults to None
        :type file_name: str, optional
        :param client_id: 티스토리 OAuth를 위한 client_id 값, defaults to None
        :type client_id: str, optional
        :param tistory_id: 티스토리 아이디입니다., defaults to None
        :type tistory_id: str, optional
        :param tistory_password: 티스토리 비밀번호입니다., defaults to None
        :type tistory_password: str, optional
        :param force_browser: 무조건 브라우저를 이용하여 설정합니다., defaults to False
        :type force_browser: bool, optional
        :raises OptionNotFoundError: 인증 과정에서 아무런 인증 옵션이 없을 때 일어나는 에러입니다.
        """
        if access_token is not None:
            self.access_token = access_token
        else:
            try_headless_auth = False

            # with a default credential file
            self._configure_with_file(DEFAULT_CONFIG_FILE_NAME, no_error=True)

            # with env vars
            self.client_id = os.environ.get(
                'PYTISTORY_CLIENT_ID', self.client_id)
            self.tistory_id = os.environ.get(
                'PYTISTORY_TISTORY_ID', self.tistory_id)
            self.tistory_password = os.environ.get(
                'PYTISTORY_TISTORY_PASSWORD', self.tistory_password)

            # with file
            if file_name is not None:
                self._configure_with_file(file_name)

            # with args
            if client_id is not None:
                self.client_id = client_id
            if tistory_id is not None:
                self.tistory_id = tistory_id
            if tistory_password is not None:
                self.tistory_password = tistory_password

            if self.client_id is None:
                raise OptionNotFoundError("Cannot configure a PyTistory.")

            if self.tistory_id is not None and self.tistory_password is not None:
                try_headless_auth = True

            # access token 받아오기
            self._set_access_token(try_headless_auth and not force_browser)

        self.blog.set_access_token(self.access_token)
        self.post.set_access_token(self.access_token)
        self.category.set_access_token(self.access_token)
        self.comment.set_access_token(self.access_token)
        self.guestbook.set_access_token(self.access_token)
