# -*- coding: utf8 -*-
"""Blog 관련 API Client 구현입니다.
"""
from .base_api import BaseAPI


class Blog(BaseAPI):
    """Blog 관련 API Client 구현입니다.

    다음과 같은 API Client가 구현되어 있습니다.

    - blog/info
        사용자의 계정에 해당하는 블로그 정보를 얻어옵니다.
    """
    kind = 'blog'

    def info(self):
        """blog/info API 구현입니다.

        블로그 정보를 받아오는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#blog-info>`_ 를 통해
        살펴보실 수 있습니다.

        :return:
            `티스토리 블로그 정보 API <http://www.tistory.com/guide/api/blog.php#blog-info>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'info')
        return self._perform('GET', url, params=self._get_default_params())
