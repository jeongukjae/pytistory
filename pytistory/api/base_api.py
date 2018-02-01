# -*- coding:utf8 -*-
#pylint: disable=R0903
# disable the pylint message R0903 `Too few public methods`
"""PyTistory BaseAPI

PyTistory에서 활용하는 API 클래스의 형태를 정의합니다.
"""
import requests

class BaseAPI:
    """다른 API들은 이 클래스를 상속받아 이용합니다.

    공통적으로 쓸 함수들을 포함합니다.
    """
    def __init__(self, access_token):
        self.access_token = access_token

    def _get_default_params(self):
        """기본적인 인자들을 반환합니다.

        access_token과 output은 기본적인 인자라 함수로 만들어서 dict로 반환하도록 했습니다.
        """
        return {
            'access_token': self.access_token,
            'output': 'json'
        }

    @staticmethod
    def _get_url(kind, action, args=None):
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
        :param args: GET 파라미터로 url 뒤에 붙는 값입니다., defaults to None
        :param args: dict, optional
        """
        args = args or {}
        querystring = '&'.join(map(lambda x: '{}={}'.format(x, args[x]), args))

        if querystring:
            querystring = '?' + querystring

        return 'https://www.tistory.com/apis/{}/{}{}'.format(kind, action, querystring)
