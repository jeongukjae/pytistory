# -*- coding: utf8 -*-
#pylint: disable=R0903
"""Comment 관련 API Client 구현입니다.
"""
import warnings
import datetime

from .base_api import BaseAPI
from ..exceptions import NoSpecifiedBlogError

class Comment(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        self.kind = 'comment'

    def list(self, post_id, blog_name=None, target_url=None):
        url = self._get_url(self.kind, 'list')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated.' +\
                ' See also `http://www.tistory.com/guide/api/comment.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        params['postId'] = post_id

        response = self._perform('GET', url, params=params)

        return response

    def newest(self, blog_name=None, target_url=None):
        url = self._get_url(self.kind, 'newest')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated.' +\
                ' See also `http://www.tistory.com/guide/api/comment.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        response = self._perform('GET', url, params=params)

        return response

    def write(self, post_id, content, blog_name=None, target_url=None, parent_id=None, secret=None):
        url = self._get_url(self.kind, 'write')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated.' +\
                ' See also `http://www.tistory.com/guide/api/comment.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        params['postId'] = post_id
        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        response = self._perform('POST', url, params=params)

        return response

    def modify(self, post_id, comment_id, content, blog_name=None, target_url=None, parent_id=None, secret=None):
        url = self._get_url(self.kind, 'modify')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated.' +\
                ' See also `http://www.tistory.com/guide/api/comment.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        params['postId'] = post_id
        params['commentId'] = comment_id
        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        response = self._perform('POST', url, params=params)

        return response

    def delete(self, post_id, comment_id, blog_name=None, target_url=None):
        url = self._get_url(self.kind, 'delete')
        params = self._get_default_params()

        if blog_name:
            params['blogName'] = blog_name
        elif target_url:
            params['targetUrl'] = target_url
            warnings.warn('A parameter `targetUrl` is deprecated.' +\
                ' See also `http://www.tistory.com/guide/api/comment.php`.')
        else:
            raise NoSpecifiedBlogError('There is no blog specified in parameters.')

        params['postId'] = post_id
        params['commentId'] = comment_id

        response = self._perform('POST', url, params=params)

        return response
