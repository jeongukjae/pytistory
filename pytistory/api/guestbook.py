# -*- coding: utf8 -*-
#pylint: disable=R0903
"""Guestbook 관련 API Client 구현입니다.
"""
import warnings
import datetime

from .base_api import BaseAPI
from ..exceptions import NoSpecifiedBlogError

class Guestbook(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Guestbook, self).__init__(*args, **kwargs)
        self.kind = 'guestbook'

    def list(self, blog_name=None, target_url=None):
        url = self._get_url(self.kind, 'list')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated. See also `http://www.tistory.com/guide/api/guestbook.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        response = self._perform('GET', url, params=params)

        return response

    def write(self, content, blog_name=None, target_url=None, parent_id=None, secret=None):
        url = self._get_url(self.kind, 'write')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated. See also `http://www.tistory.com/guide/api/guestbook.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        response = self._perform('POST', url, params=params)

        return response

    def modify(self, guestbook_id, content, blog_name=None, target_url=None, parent_id=None, secret=None):
        url = self._get_url(self.kind, 'modify')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated. See also `http://www.tistory.com/guide/api/guestbook.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        params['guestbookId'] = guestbook_id
        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        response = self._perform('POST', url, params=params)

        return response

    def delete(self, guestbook_id, blog_name=None, target_url=None):
        url = self._get_url(self.kind, 'delete')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated. See also `http://www.tistory.com/guide/api/guestbook.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        params['guestbookId'] = guestbook_id

        response = self._perform('POST', url, params=params)

        return response
