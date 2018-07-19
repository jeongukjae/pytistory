# -*- coding: utf8 -*-
"""Post 관련 API Client 구현입니다.
"""
import datetime

from .base_api import BaseAPI


class Post(BaseAPI):
    """Post 관련 API Client 구현입니다.

    다음과 같은 API Client가 구현되어 있습니다.

    - post/list
        최근 게시물 목록을 가져올 수 있는 API입니다.
    - post/write
        게시글을 작성할 수 있는 API입니다.
    - post/modify
        작성된 게시글을 수정할 수 있는 API입니다.
    - post/read
        단일 게시글을 읽을 수 있는 API입니다.
    - post/attach
        파일을 첨부 할 수 있는 API입니다.
    - post/delete
        단일 게시글을 삭제할 수 있는 API입니다.
    """
    # pylint: disable=too-many-arguments
    kind = 'post'

    def list(self, blog_name=None, target_url=None):
        """post/list API 구현입니다.

        최근 게시물 목록을 가져올 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/post.php#post-list>`_ 를 통해
        살펴보실 수 있습니다.

        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :raise TypeError: 인자의 타입이 잘못되었을 때 일어납니다.
        :return:
            `최근 게시글 목록 API <http://www.tistory.com/guide/api/post.php#post-list>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'list')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        response = self._perform('GET', url, params=params)

        return response

    def write(self, title, blog_name=None, target_url=None, visibility=0,
              published=None, category=0, content=None, slogan=None, tag=None):
        """post/list API 구현입니다.

        게시글을 작성할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/post.php#post-write>`_ 를 통해
        살펴보실 수 있습니다.

        :param title: 포스트 제목입니다.
        :type title: str
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :param visibility:
            - 0: 비공개
            - 1: 보호
            - 2: 공개
            - 3: 발행

            defaults to 0
        :type visibility: int, optional
        :param published: 발행 시간. 만약 설정시 예약 발행이 됨., defaults to None
        :type published: :class:`datetime.datetime`, optional
        :param category: 0은 분류없음. 값 설정시 카테고리 설정, defaults to 0
        :type category: int, optional
        :param content: 글 내용, defaults to None
        :type content: str, optional
        :param slogan: 문자 주소. 이는 아마 블로그 주소 형식을 문자로 설정했을 때의 값인 듯 함., defaults to None
        :type slogan: str, optional
        :param tag: 게시글에 태그를 설정합니다, defaults to None
        :type tag: list, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :raise TypeError: 인자의 타입이 잘못되었을 때 일어납니다.
        :return:
            `최근 게시글 목록 API <http://www.tistory.com/guide/api/post.php#post-write>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'write')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        if isinstance(visibility, int) and visibility >= 0 and visibility <= 3:
            params['visibility'] = visibility
        else:
            raise TypeError('A visibility must be 0, 1, 2, or 3.')

        if published:
            if isinstance(published, datetime.datetime):
                params['published'] = published.timestamp()
            else:
                raise TypeError('A published must be a datetime object')

        # dangerous-default-value
        if tag is None:
            tag = []

        if isinstance(tag, list):
            params['tag'] = ','.join(tag)
        else:
            raise TypeError('A tag must be a list.')

        params['title'] = title
        params['category'] = category
        params['content'] = content
        params['slogan'] = slogan

        response = self._perform('POST', url, data=params)

        return response

    def modify(self, title, post_id, blog_name=None, target_url=None, visibility=0,
               category=0, content=None, slogan=None, tag=None):
        """post/modify API 구현입니다.

        작성된 게시글을 수정할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/post.php#post-modify>`_ 를 통해
        살펴보실 수 있습니다.

        :param title: 포스트 제목입니다.
        :type title: str
        :param post_id: 포스트 고유번호입니다.
        :type title: int
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :param visibility:
            - 0: 비공개
            - 1: 보호
            - 2: 공개
            - 3: 발행

            defaults to 0
        :type visibility: int, optional
        :param category: 0은 분류없음. 값 설정시 카테고리 설정, defaults to 0
        :type category: int, optional
        :param content: 글 내용, defaults to None
        :type content: str, optional
        :param slogan: 문자 주소. 이는 아마 블로그 주소 형식을 문자로 설정했을 때의 값인 듯 함., defaults to None
        :type slogan: str, optional
        :param tag: 게시글에 태그를 설정합니다, defaults to None
        :type tag: list, optional
        :raise NoSpecifiedBlog: 블로그 정보를 설정할 수 없을 때 일어납니다.
        :raise TypeError: 인자의 타입이 잘못되었을 때 일어납니다.
        :return:
            `최근 게시글 목록 API <http://www.tistory.com/guide/api/post.php#post-modify>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'modify')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        if isinstance(visibility, int) and visibility >= 0 and visibility <= 3:
            params['visibility'] = visibility
        else:
            raise TypeError('A visibility must be 0, 1, 2, or 3.')
        if tag is None:
            tag = []
        if isinstance(tag, list):
            params['tag'] = ','.join(tag)
        else:
            raise TypeError('A tag must be a list.')

        params['title'] = title
        params['postId'] = post_id
        params['category'] = category
        params['content'] = content
        params['slogan'] = slogan

        response = self._perform('POST', url, data=params)

        return response

    def read(self, post_id, blog_name=None, target_url=None):
        """post/read API 구현입니다.

        단일 게시글을 읽을 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/post.php#post-read>`_ 를 통해
        살펴보실 수 있습니다.

        :param post_id: 게시글 번호
        :type post_id: int
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raises NoSpecifiedBlogError: 해당하는 블로그가 존재하지 않을 때 일어나는 에러입니다.
        :return:
            `글 읽기 API  <http://www.tistory.com/guide/api/post.php#post-read>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'read')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['postId'] = post_id

        response = self._perform('GET', url, params=params)

        return response

    def attach(self, uploaded_file, blog_name=None, target_url=None):
        """post/attach API 구현입니다.

        파일을 첨부 할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/post.php#post-attach>`_ 를 통해
        살펴보실 수 있습니다.

        :param uploaded_file: 업로드할 파일의 경로입니다.
        :type uploaded_file: str
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raises NoSpecifiedBlogError: 해당하는 블로그가 존재하지 않을 때 일어나는 에러입니다.
        :return:
            `파일 첨부 API  <http://www.tistory.com/guide/api/post.php#post-attach>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'attach')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        with open(uploaded_file, 'rb') as f:
            files = {'uploadedfile': f}
            response = self._perform('POST', url, data=params, files=files)

        return response

    def delete(self, post_id, blog_name=None, target_url=None):
        """post/delete API 구현입니다.

        단일 게시글을 삭제할 수 있는 API입니다. 해당 API에 관한 정보는
        `링크 <http://www.tistory.com/guide/api/post.php#post-delete>`_ 를 통해
        살펴보실 수 있습니다.

        :param post_id: 삭제할 게시글 번호입니다.
        :type post_id: int
        :param blog_name: 블로그 명입니다., defaults to None
        :type blog_name: str, optional
        :param target_url: 블로그의 url입니다. deprecated된 옵션입니다., defaults to None
        :type target_url: str, optional
        :raises NoSpecifiedBlogError: 해당하는 블로그가 존재하지 않을 때 일어나는 에러입니다.
        :return:
            `글 삭제 API  <http://www.tistory.com/guide/api/post.php#post-delete>`_ 링크에서
            어떤 데이터가 넘어오는 지 알 수 있습니다.
        :rtype: dict
        """
        url = self._get_url(self.kind, 'delete')
        params = self._get_default_params()
        self._set_blog_name(params, blog_name, target_url)

        params['postId'] = post_id

        response = self._perform('POST', url, data=params)

        return response
