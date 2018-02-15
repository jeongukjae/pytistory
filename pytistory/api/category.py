# -*- coding: utf8 -*-
#pylint: disable=R0903
"""Category 관련 API Client 구현입니다.
"""
import warnings
import datetime

from .base_api import BaseAPI
from ..exceptions import NoSpecifiedBlogError

class Category(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.kind = 'category'

    def list(self, blog_name=None, target_url=None):
        url = self._get_url(self.kind, 'delete')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated. See also `http://www.tistory.com/guide/api/category.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        response = self._perform('GET', url, params=params)

        return response
