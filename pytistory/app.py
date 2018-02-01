# -*- coding: utf8 -*-
"""PyTistory를 정의하는 모듈입니다.
"""
import configparser
import multiprocessing
import webbrowser
import time

from .exceptions import ConfigurationError
from .callback import CallbackServer

TISTORY_AUTHORIZE_URL = 'https://www.tistory.com/oauth/authorize'
TISTORY_AUTHORIZE_PARAMS = '?client_id={0}&response_type=token' +\
    '&redirect_uri=http://0.0.0.0:5000/callback'

CONFIG_SECTION_NAME = 'pytistory'
CONFIG_CLIENT_ID = 'client_id'
CONFIG_SECRET_KEY = 'secret_key'
CONFIG_ACCESS_TOKEN = 'access_token'

TISTORY_API_BASE_URL = 'https://www.tistory.com/apis/{}/{}'

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
    def __init__(self):
        self.file_name = ''
        self.client_id = ''
        self.secret_key = ''
        self.access_token = ''

    def _read_configuration_file(self):
        """Configuration File을 읽고, ConfigParser를 반환합니다.

        self.file_name에 해당하는 파일을 읽고, 해당 파일의 설정값들을 반환합니다.
        만약, :class:`PyTistory`에서 원하는 내용의 설정 키값들이 없다면, ConfigurationError를
        일으킵니다.

        :raises ConfigurationError: 설정파일에서 pytistory 섹션을 찾을 수 없을 때 일어납니다.
        :raises ConfigurationError: pytistory 섹션에서 client_id 키를 찾을 수 없을 때 일어납니다.
        :raises ConfigurationError: pytistory 섹션에서 secret_key 키를 찾을 수 없을 때 일어납니다.
        :return: 파일에서 읽어들인 config를 반환합니다.
        :rtype: :class:`configparser.ConfigParser`
        """
        config = configparser.ConfigParser()

        config.read(self.file_name)

        if CONFIG_SECTION_NAME not in config:
            raise ConfigurationError('Cannot find a `{}` section in `{}`.'.\
                format(CONFIG_SECTION_NAME, self.file_name))
        if CONFIG_CLIENT_ID not in config[CONFIG_SECTION_NAME]:
            raise ConfigurationError('Cannot find a tistory client id in `{}`.'\
                .format(self.file_name))
        if CONFIG_SECRET_KEY not in config[CONFIG_SECTION_NAME]:
            raise ConfigurationError('Cannot find a tistory secret key in `{}`.'\
                .format(self.file_name))

        return config

    def _set_access_token(self):
        """Tistory의 access_token을 설정하는 함수입니다.

        `CallbackServer`를 구동시킨 후, 티스토리 인증 창을 브라우저를 통해 엽니다.
        그 후 인증이 되었다면, access_token을 받아옵니다.

        :raises ConfigurationError: 만약 access_token이 정상적으로 받아와지지 않았을 경우입니다.
        """
        multiprocessing_manager = multiprocessing.Manager()
        namespace = multiprocessing_manager.Namespace()
        event = multiprocessing.Event()

        process = multiprocessing.Process(target=callback_process, args=(namespace, event))
        process.start()

        time.sleep(2)

        webbrowser.open_new(TISTORY_AUTHORIZE_URL + TISTORY_AUTHORIZE_PARAMS.format(self.client_id))

        event.wait()
        if hasattr(namespace, 'access_token'):
            self.access_token = namespace.access_token #pylint: disable=E1101
        else:
            raise ConfigurationError('Cannot get the access token from a server.')

        process.join()

    def configure(self, **kwargs):
        """Tistory OAuth 2.0 인증을 실행하는 함수입니다.

        `Tistory Open API OAuth 인증 <http://www.tistory.com/guide/api/oauth>`_에
        해당하는 구현이고, Client-side flow방식을 이용하였습니다.
        티스토리 client_id, secret_key 값을 파일에서 읽거나,
        인자에서 받아서 인증을 하게 됩니다.

        :raises ConfigurationError: 설정이 불가능할 때 일어납니다.
        """
        if 'configure_file_name' in kwargs:
            # 파일에서 설정읽기
            self.file_name = kwargs['configure_file_name']
            config = self._read_configuration_file()

            self.client_id = config[CONFIG_SECTION_NAME][CONFIG_CLIENT_ID]
            self.secret_key = config[CONFIG_SECTION_NAME][CONFIG_SECRET_KEY]
        elif 'client_id' in kwargs and 'secret_key' in kwargs:
            self.client_id = kwargs['client_id']
            self.secret_key = kwargs['secret_key']
        else:
            raise ConfigurationError('Cannot configure a PyTistory.')

        # access token 받아오기
        self._set_access_token()

        if self.file_name:
            config[CONFIG_SECTION_NAME][CONFIG_ACCESS_TOKEN] = self.access_token
            with open(self.file_name, 'w') as config_file:
                config.write(config_file)
