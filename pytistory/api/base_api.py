# -*- coding:utf8 -*-
#pylint: disable=R0903
# disable the pylint message R0903 `Too few public methods`
"""PyTistory BaseAPI

PyTistory에서 활용하는 API 클래스의 형태를 정의합니다.
"""
import json
import warnings
import requests

from ..exceptions import ParsingError, TokenNotFoundError, NoSpecifiedBlogError

class BaseAPI:
    """다른 API들은 이 클래스를 상속받아 이용합니다.

    공통적으로 쓸 함수들을 포함합니다.
    """
    kind = ''

    def __init__(self, access_token=None):
        self.access_token = None

        if access_token:
            self.set_access_token(access_token)

    def _set_blog_name(self, params, blog_name, target_url):
        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated.' +\
                ' See also `http://www.tistory.com/guide/api/{0}.php`.'.format(self.kind))
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

    def set_access_token(self, access_token):
        """Access Token을 설정합니다.

        :param access_token: Tistory 인증 후 반환되는 Access Token입니다.
        :type access_token: str
        """
        self.access_token = access_token

    def _get_default_params(self):
        """기본적인 인자들을 반환합니다.

        access_token과 output은 기본적인 인자라 함수로 만들어서 dict로 반환하도록 했습니다.
        """
        if self.access_token is None:
            raise TokenNotFoundError('You have not set up an `Access Token` yet.' +\
                ' Call configure() first.')
        return {
            'access_token': self.access_token,
            'output': 'json'
        }

    @staticmethod
    def _perform(method, url, **kwargs):
        """Tistory API 서버에 요청하고 응답을 받아와주는 함수입니다.

        만약 Status가 200이 아니라면 Exception을 일으키고,
        맞다면 응답 결과를 반환합니다.

        :param method: HTTP Method명을 나타냅니다.
        :type method: str
        :param url: API URL을 나타냅니다.
        :type url: str
        :param params: querystring에 들어갈 인지입니다.
        :type params: dict
        :param data: HTTP Body에 들어갈 인자입니다.
        :type data: dict

        :raises ParsingError: Status를 찾을 수 없거나, 200이 아닐 경우 일어납니다.
        :return: API의 결과값입니다.
        :rtype: dict
        """
        response = requests.request(method, url, **kwargs)
        result = json.loads(response.text)

        if 'tistory' in result and 'status' in result['tistory']:
            if result['tistory']['status'] == '200':
                return result['tistory']

        raise ParsingError('Status Code is not 200.\nrequest : {} {}, {}\nresponse result: {}'.format(method, url, kwargs, result))

    @staticmethod
    def _get_url(kind, action):
        """Tistory API URL을 만드는 함수입니다.

        Kind, Action, Args 인자들을 종합하여 api url을 만들어 반환합니다.
        Kind, Action, Args 값은 Tistory 공식 문서를 참고하시기 바랍니다.

        .. seealso::
            `Tistory 오픈 API 가이드 홈 <http://www.tistory.com/guide/api/index>`_

        :param kind:
            API의 큰 분류라 보면 됩니다. `blog`, `post`, `category`, `comment`,
            `guestbook` 이 있습니다.
        :type kind: str
        :param action:
            API의 작은 분류입니다. 각각 kind 별로 해당하는 값이 존재합니다.
        :type action: str
        """
        return 'https://www.tistory.com/apis/{}/{}'.format(kind, action)
