# -*- coding: utf8 -*-
#pylint: disable=too-many-arguments
"""Comment 관련 API Client 구현입니다.
"""
from .base_api import BaseAPI


class Comment(BaseAPI):
    """Comment 관련 API Client 구현입니다.

    다음과 같은 API Client가 구현되어 있습니다.

    - comment/list
        단일 게시글에 포함된 댓글 정보를 조회할 수 있는 API입니다.
    - comment/newest
        블로그내 최근 댓글을 조회할 수 있는 API입니다.
    - comment/write
        단일 게시글 및 단일 댓글에 댓글을 작성할 수 있는 API입니다.
    - comment/modify
        이미 작성된 댓글을 수정할 수 있는 API입니다.
    - comment/delete
        댓글을 삭제할 수 있는 API입니다.
    """
    kind = 'comment'

    def list(self, post_id, blog_name=None, target_url=None):
        """comment/list API 구현입니다.

        단일 게시글에 포함된 댓글 정보를 조회할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#comment-list>`_ 를 통해
        살펴보실 수 있습니다.

        :param post_id: 게시글 ID입니다.
        :type post_id: int
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `게시글 댓글 목록 API <http://www.tistory.com/guide/api/blog.php#comment-list>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'list')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['postId'] = post_id

        return self._perform('GET', url, params=params)

    def newest(self, blog_name=None, target_url=None):
        """comment/newest API 구현입니다.

        블로그내 최근 댓글을 조회할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#comment-newest>`_ 를 통해
        살펴보실 수 있습니다.

        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `최근 댓글 목록 API <http://www.tistory.com/guide/api/blog.php#comment-newest>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'newest')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        return self._perform('GET', url, params=params)

    def write(self, post_id, content, blog_name=None, target_url=None, parent_id=None, secret=None):
        """comment/write API 구현입니다.

        단일 게시글 및 단일 댓글에 댓글을 작성할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#comment-write>`_ 를 통해
        살펴보실 수 있습니다.

        :param post_id: 게시글 ID입니다.
        :type post_id: int
        :param content: 해당 댓글의 내용입니다.
        :type content: str
        :param parent_id: 부모 댓글 id입니다. 댓글의 댓글일 경우만 사용합니다., defaults to None
        :type parent_id: int, optional
        :param secret: 비밀글 여부입니다. 1일 경우 설정됩니다., defaults to None
        :type secret: int, optional
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `댓글 작성 API <http://www.tistory.com/guide/api/blog.php#comment-write>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'write')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['postId'] = post_id
        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        return self._perform('POST', url, data=params)

    def modify(self, post_id, comment_id, content, blog_name=None, target_url=None,
               parent_id=None, secret=None):
        """comment/modify API 구현입니다.

        이미 작성된 댓글을 수정할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#comment-modify>`_ 를 통해
        살펴보실 수 있습니다.

        :param post_id: 게시글 ID입니다.
        :type post_id: int
        :param comment_id: 수정하려는 댓글 id입니다.
        :type comment_id: int
        :param content: 해당 댓글의 내용입니다.
        :type content: str
        :param parent_id: 부모 댓글 id입니다. 댓글의 댓글일 경우만 사용합니다., defaults to None
        :type parent_id: int, optional
        :param secret: 비밀글 여부입니다. 1일 경우 설정됩니다., defaults to None
        :type secret: int, optional
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `댓글 수정 API <http://www.tistory.com/guide/api/blog.php#comment-modify>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'modify')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['postId'] = post_id
        params['commentId'] = comment_id
        params['content'] = content

        if parent_id:
            params['parentId'] = parent_id
        if secret:
            params['secret'] = secret

        return self._perform('POST', url, data=params)

    def delete(self, post_id, comment_id, blog_name=None, target_url=None):
        """comment/delete API 구현입니다.

        댓글을 삭제할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/blog.php#comment-delete>`_ 를 통해
        살펴보실 수 있습니다.

        :param post_id: 게시글 ID입니다.
        :type post_id: int
        :param comment_id: 삭제하려는 댓글 id입니다.
        :type comment_id: int
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :return:
            `댓글 삭제 API <http://www.tistory.com/guide/api/blog.php#comment-delete>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'delete')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['postId'] = post_id
        params['commentId'] = comment_id

        return self._perform('POST', url, data=params)
