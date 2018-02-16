# -*- coding: utf8 -*-
#pylint: disable=too-many-arguments
"""Guestbook 관련 API Client 구현입니다.
"""
from .base_api import BaseAPI

class Guestbook(BaseAPI):
    """Guestbook 관련 API Client 구현입니다.

    다음과 같은 API Client가 구현되어 있습니다.

    - guestbook/list
        블로그내 방명록을 조회할 수 있는 API입니다.
    - guestbook/write
        방명록 또는 방명록의 답변을 작성할 수 있는 API입니다.
    - guestbook/modify
        이미 작성된 방명록을 수정할 수 있는 API입니다.
    - guestbook/delete
        방명록을 삭제할 수 있는 API입니다.
    """
    kind = 'guestbook'

    def list(self, blog_name=None, target_url=None):
        """guestbook/list API 구현입니다.

        블로그내 방명록을 조회할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#guestbook-list>`_ 를 통해
        살펴보실 수 있습니다.

        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `방명록 목록 API <http://www.tistory.com/guide/api/blog.php#guestbook-list>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'list')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        return self._perform('GET', url, params=params)

    def write(self, content, blog_name=None, target_url=None, parent_id=None, secret=None):
        """guestbook/write API 구현입니다.

        방명록 또는 방명록의 답변을 작성할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#guestbook-write>`_ 를 통해
        살펴보실 수 있습니다.

        :param content: 방명록 내용입니다.
        :type content: str
        :param parent_id: 부모 방명록 id입니다. 방명록의 답글일 경우만 사용, defaults to None
        :type parent_id: int, optional
        :param secret: 비밀글 여부입니다. 1일 경우 설정됩니다., defaults to None
        :type secret: int, optional
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `방명록 작성 API <http://www.tistory.com/guide/api/blog.php#guestbook-write>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'write')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        return self._perform('POST', url, data=params)

    def modify(self, guestbook_id, content, blog_name=None,
               target_url=None, parent_id=None, secret=None):
        """guestbook/modify API 구현입니다.

        이미 작성된 방명록을 수정할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#guestbook-modify>`_ 를 통해
        살펴보실 수 있습니다.

        :param guestbook_id: 수정하려는 방명록의 ID입니다.
        :type guestbook_id: int
        :param content: 방명록 내용입니다.
        :type content: str
        :param parent_id: 부모 방명록 id입니다. 방명록의 답글일 경우만 사용, defaults to None
        :type parent_id: int, optional
        :param secret: 비밀글 여부입니다. 1일 경우 설정됩니다., defaults to None
        :type secret: int, optional
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `방명록 수정 API <http://www.tistory.com/guide/api/blog.php#guestbook-modify>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'modify')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['guestbookId'] = guestbook_id
        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        return self._perform('POST', url, data=params)

    def delete(self, guestbook_id, blog_name=None, target_url=None):
        """guestbook/delete API 구현입니다.

        방명록을 삭제할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#guestbook-delete>`_ 를 통해
        살펴보실 수 있습니다.

        :param guestbook_id: 삭제하려는 방명록의 ID입니다.
        :type guestbook_id: int
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `방명록 삭제 API <http://www.tistory.com/guide/api/blog.php#guestbook-delete>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'delete')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['guestbookId'] = guestbook_id

        return self._perform('POST', url, data=params)
