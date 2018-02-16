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
TISTORY_AUTHORIZE_PARAMS = '?client_id={0}&response_type=token' +\
    '&redirect_uri=http://0.0.0.0:5000/callback'

CONFIG_SECTION_NAME = 'pytistory'
CONFIG_CLIENT_ID = 'client_id'
CONFIG_SECRET_KEY = 'secret_key'
CONFIG_ACCESS_TOKEN = 'access_token'
CONFIG_TISTORY_ID = 'tistory_id'
CONFIG_TISTORY_PASSWORD = 'tistory_password'

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
        self.file_name = ''
        self.client_id = ''
        self.secret_key = ''
        self.access_token = ''
        self.tistory_id = ''
        self.tistory_password = ''

        self.blog = Blog()
        self.post = Post()
        self.category = Category()
        self.comment = Comment()
        self.guestbook = Guestbook()

    def _read_configuration_file(self, headless_auth=False):
        """Configuration File을 읽고, ConfigParser를 반환합니다.

        self.file_name에 해당하는 파일을 읽고, 해당 파일의 설정값들을 반환합니다.
        만약, :class:`PyTistory`에서 원하는 내용의 설정 키값들이 없다면, Exception을
        일으킵니다.

        :param headless_auth: Headless 브라우저를 사용해서 인증을 시도할 때 이 인자를 사용합니다., defaults to False
        :param headless_auth: bool, optional
        :raises InvalidSectionError: 설정파일에서 pytistory 섹션을 찾을 수 없을 때 일어납니다.
        :raises InvalidNameError: pytistory 섹션에서 client_id 키를 찾을 수 없을 때 일어납니다.
        :return: 파일에서 읽어들인 config를 반환합니다.
        :rtype: :class:`configparser.ConfigParser`
        """
        config = configparser.ConfigParser()

        config.read(self.file_name)

        if CONFIG_SECTION_NAME not in config:
            raise InvalidSectionError('Cannot find a `{}` section in `{}`.'.\
                format(CONFIG_SECTION_NAME, self.file_name))
        if CONFIG_CLIENT_ID not in config[CONFIG_SECTION_NAME]:
            raise InvalidNameError('Cannot find a tistory client id in `{}`.'\
                .format(self.file_name))
        if CONFIG_SECRET_KEY not in config[CONFIG_SECTION_NAME]:
            raise InvalidNameError('Cannot find a tistory secret key in `{}`.'\
                .format(self.file_name))
        if headless_auth:
            if CONFIG_TISTORY_ID not in config[CONFIG_SECTION_NAME]:
                raise InvalidNameError('Cannot find a tistory user id in `{}`.'\
                    .format(self.file_name))
            if CONFIG_TISTORY_PASSWORD not in config[CONFIG_SECTION_NAME]:
                raise InvalidNameError('Cannot find a tistory password in `{}`.'\
                    .format(self.file_name))

        return config

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
        :raises ImportError: selenium을 import할 수 없는 경우입니다.
        :raises WebDriverError: Headless Chrome을 사용할 수 없는 경우입니다.
        :raises EmailAuthError: 티스토리 인증 중 이메일 인증이 필요한 경우입니다.
        :raises TokenNotFoundError: 만약 access_token이 정상적으로 받아와지지 않았을 경우입니다.
        """
        multiprocessing_manager = multiprocessing.Manager()
        namespace = multiprocessing_manager.Namespace()
        event = multiprocessing.Event()

        process = multiprocessing.Process(target=callback_process, args=(namespace, event))
        process.start()

        while not self._is_listening():
            time.sleep(0.1)

        request_uri = TISTORY_AUTHORIZE_URL + TISTORY_AUTHORIZE_PARAMS.format(self.client_id)

        if not headless_auth:
            webbrowser.open_new(request_uri)
        else:
            try:
                from selenium import webdriver
                from selenium.common.exceptions import (WebDriverException, NoSuchWindowException,
                                                        NoSuchElementException)
            except ImportError:
                raise ImportError('Cannot import selenum.\n' +\
                    'The headless authentication option need selenium.')
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                driver = webdriver.Chrome(options=options)
            except WebDriverException:
                raise WebDriverError('Cannot open Chrome Headless. Please install Chrome Headless.')

            driver.get(request_uri)
            driver.find_element_by_name('loginId').send_keys(self.tistory_id)
            driver.find_element_by_name('password').send_keys(self.tistory_password)
            driver.find_element_by_xpath('//*[@id="authForm"]/fieldset/div/button').click()

            try:
                current_url = driver.current_url
            except NoSuchWindowException:
                current_url = ''

            # 비밀번호 변경하라는 창
            if current_url.split('?')[0].endswith('outdated'):
                # 다음에 변경하기
                driver.find_element_by_xpath('//*[@id="passwordChangeForm"]/fieldset/div/a').click()
            elif current_url.endswith('auth/login'):
                try:
                    driver.find_element_by_xpath('//*[@id="authForm"]/fieldset' +\
                        '/div/div[contains(@class, \'box_noti\')]')

                    # 만약 위에서 오류가 안나면 ID/PW 오류.
                    # 나면, 이메일 인증 오류
                    raise InvalidAccountError('Invalid Account Information. Please enter correct' +\
                        ' ID and PW.')
                except NoSuchElementException:
                    raise EmailAuthError('Email authentication is required to log in to Tistory.')
                finally:
                    process.terminate()
                    process.join()
            elif not current_url.startswith('http://0.0.0.0:5000'):
                process.terminate()
                process.join()
                raise ConfigurationError('Invalid ID format or Invalid client key and secret.')

            driver.quit()

        event.wait()
        if hasattr(namespace, 'access_token'):
            self.access_token = namespace.access_token #pylint: disable=E1101
            # disable the pylint message E1101 `Instance of 'Namespace'
            # has no 'access_token' member'`
            # checked in if statement
        else:
            raise TokenNotFoundError('Cannot get the access token from a server.')

        process.join()

    #pylint: disable=too-many-arguments
    def configure(self, configure_file_name=None,
                  client_id=None, secret_key=None,
                  tistory_id=None, tistory_password=None):
        """Tistory OAuth 2.0 인증을 실행하는 함수입니다.

        `Tistory Open API OAuth 인증 <http://www.tistory.com/guide/api/oauth>`_에
        해당하는 구현이고, Client-side flow방식을 이용하였습니다.
        티스토리 client_id, secret_key 값을 파일에서 읽거나,
        인자에서 받거나, 환경변수에서 받아서 인증을 하게 됩니다.

        환경 변수의 KEY는 `PYTISTORY_CLIENT_ID`, `PYTISTORY_SECRET_KEY` 를
        사용합니다.

        :param configure_file_name: configure 파일 이름, defaults to None
        :type configure_file_name: str, optional
        :param client_id: 티스토리 OAuth를 위한 client_id 값, defaults to None
        :type client_id: str, optional
        :param secret_key: 티스토리 OAuth를 위한 secret_key 값, defaults to None
        :type secret_key: str, optional
        :param tistory_id: 티스토리 아이디입니다., defaults to None
        :type tistory_id: str, optional
        :param tistory_password: 티스토리 비밀번호입니다., defaults to None
        :type tistory_password: str, optional
        :raises OptionNotFoundError: 인증 과정에서 아무런 인증 옵션이 없을 때 일어나는 에러입니다.
        """
        headless_auth = False

        if configure_file_name is not None:
            # 파일에서 설정읽기
            self.file_name = configure_file_name
            config = self._read_configuration_file(headless_auth)

            self.client_id = config[CONFIG_SECTION_NAME][CONFIG_CLIENT_ID]
            self.secret_key = config[CONFIG_SECTION_NAME][CONFIG_SECRET_KEY]
            self.tistory_id = config[CONFIG_SECTION_NAME][CONFIG_TISTORY_ID]
            self.tistory_password = config[CONFIG_SECTION_NAME][CONFIG_TISTORY_PASSWORD]
            if self.tistory_id and self.tistory_password:
                headless_auth = True
        elif client_id is not None and secret_key is not None:
            self.client_id = client_id
            self.secret_key = secret_key
            if tistory_id is not None and tistory_password is not None:
                headless_auth = True
                self.tistory_id = tistory_id
                self.tistory_password = tistory_password
        else:
            self.client_id = os.environ.get('PYTISTORY_CLIENT_ID')
            self.secret_key = os.environ.get('PYTISTORY_SECRET_KEY')

            if self.client_id is None or self.secret_key is None:
                raise OptionNotFoundError('Cannot configure a PyTistory.')

            self.tistory_id = os.environ.get('PYTISTORY_TISTORY_ID')
            self.tistory_password = os.environ.get('PYTISTORY_TISTORY_PASSWORD')

            if self.tistory_id and self.tistory_password:
                headless_auth = True

        # access token 받아오기
        self._set_access_token(headless_auth)

        self.blog.set_access_token(self.access_token)
        self.post.set_access_token(self.access_token)
        self.category.set_access_token(self.access_token)
        self.comment.set_access_token(self.access_token)
        self.guestbook.set_access_token(self.access_token)

        if self.file_name:
            config[CONFIG_SECTION_NAME][CONFIG_ACCESS_TOKEN] = self.access_token
            with open(self.file_name, 'w') as config_file:
                config.write(config_file)
