# -*- coding: utf8 -*-
"""Category 관련 API Client 구현입니다.
"""
from .base_api import BaseAPI

class Category(BaseAPI):
    """Category 관련 API Client 구현입니다.

    다음과 같은 API Client가 구현되어 있습니다.

    - category/list
        카테고리 목록을 가져올 수 있는 API입니다.
    """
    kind = 'category'

    def list(self, blog_name=None, target_url=None):
        """category/list API 구현입니다.

        카테고리 목록을 가져올 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#category-list>`_ 를 통해
        살펴보실 수 있습니다.

        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `카테고리 목록 API <http://www.tistory.com/guide/api/blog.php#category-list>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'list')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        return self._perform('GET', url, params=params)
