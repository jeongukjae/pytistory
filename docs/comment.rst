Comment API
===========

게시글 댓글 정보 조회
-----------------------

단일 게시글에 포함된 댓글 정보를 조회할 수 있는 API입니다. 해당 API에 관한 정보는
`단일 게시글 댓글 조회 API <http://www.tistory.com/guide/api/blog.php#comment-list>`_ 를 통해
살펴보실 수 있습니다.

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure()

  response = pytistory.comment.list(4, blog_name='oauth')

결과값은 아래처럼 받을 수 있습니다.

.. code-block:: json

  {
    "status": "200",
    "item": {
      "url": "http://oauth.tistory.com/4",
      "secondaryUrl": "",
      "postId": "4",
      "totalCount": "3",
      "comments": {
        "comment": [
          {
            "id": "8176918",
            "date": "1303796711",
            "name": "지나다가",
            "parentId": "",
            "homepage": "http://someurl.com",
            "visibility": "2",
            "comment": "좋은 글 감사합니다.",
            "open": "Y"
          },
          {
            "id": "8176923",
            "date": "1303796801",
            "name": "글쎄요",
            "parentId": "",
            "homepage": "http://shesgone.com",
            "visibility": "2",
            "comment": " 제 홈에 와서 구경해보세요^_^",
            "open": "N"
          },
          {
            "id": "8176926",
            "date": "1303796900",
            "name": "Tistory API",
            "parentId": "8176918",
            "homepage": "http://oauth.tistory.com",
            "visibility": "2",
            "comment": "비루한 글에 칭찬을 하시니 몸둘바를 모르.. 지 않아!",
            "open": "Y"
          }
        ]
      }
    }
  }

최근 댓글 조회
------------------

블로그내 최근 댓글을 조회할 수 있는 API입니다. 해당 API에 관한 정보는
`최근 댓글 조회 API <http://www.tistory.com/guide/api/blog.php#comment-newest>`_ 를 통해
살펴보실 수 있습니다.

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure()

  response = pytistory.comment.newest(blog_name='oauth')

결과값은 아래처럼 받을 수 있습니다.

.. code-block:: json

  {
    "status": "200",
    "item": {
      "url": "http://oauth.tistory.com",
      "secondaryUrl": "",
      "comments": {
        "comment": [
          {
            "id": "8176926",
            "date": "1303796900",
            "postId": "4",
            "name": "Tistory API",
            "homepage": "http://oauth.tistory.com",
            "comment": "비루한 글에 칭찬을 하시니 몸둘바를 모르.. 지 않아!",
            "open": "Y",
            "link": "http://oauth.tistory.com/4#comment8176926"
          },
          {
            "id": "8176923",
            "date": "1303796801",
            "postId": "4",
            "name": "글쎄 요",
            "homepage": "http://shesgone.com",
            "comment": "제 홈에 와서 구경해보세요^_^",
            "open": "N",
            "link": "http://oauth.tistory.com/4#comment8176923"
          },
          {
            "id": "8176918",
            "date": "1303796711",
            "postId": "4",
            "name": "지나다가",
            "homepage": "http://someurl.com",
            "comment": "좋은 글 감사합니다.",
            "open": "Y",
            "link": "http://oauth.tistory.com/4#comment8176918"
          }
        ]
      }
    }
  }

댓글 작성
------------------

단일 게시글 및 단일 댓글에 댓글을 작성할 수 있는 API입니다. 해당 API에 관한 정보는
`댓글 작성 API <http://www.tistory.com/guide/api/blog.php#comment-write>`_ 를 통해
살펴보실 수 있습니다.

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure()

  response = pytistory.comment.write(4,
                                    'some-comment-content',
                                    blog_name='oauth',
                                    parent_id=12,
                                    secret=1)

인자값은 ``post_id``\ 값과 댓글의 내용을 먼저 넣어줍니다.
``parent_id``\ 댓글의 답글일 경우 설정하는 optional 값입니다.
``secret``\ 인자 경우는 1일 경우 비밀 댓글이 됩니다.

결과값은 아래처럼 받을 수 있습니다.

.. code-block:: json

  {
    "status": "200",
    "commentUrl": "http://oauth.tistory.com/4#comment8176976",
    "result": "OK"
  }

댓글 수정
------------------

이미 작성된 댓글을 수정할 수 있는 API입니다. 해당 API에 관한 정보는
`댓글 수정 API <http://www.tistory.com/guide/api/blog.php#comment-modify>`_ 를 통해
살펴보실 수 있습니다.

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure()

  response = pytistory.comment.modify(4,
                                    8176976,
                                    'some-comment-content',
                                    blog_name='oauth',
                                    parent_id=12)

수정의 경우이므로, 게시글 id (``post_id``\)와 댓글 id (``comment_id``\), 수정할 내용을 전달해줍니다.
그 뒤로는 ``secret``\이 빠진 점을 제외하면 댓글 작성과 동일합니다.

결과값은 아래처럼 받을 수 있습니다.

.. code-block:: json

  {
    "status": "200",
    "commentUrl": "http://oauth.tistory.com/4#comment8176976",
    "result": "OK"
  }

댓글 삭제
------------------

댓글을 삭제할 수 있는 API입니다. 해당 API에 관한 정보는
`댓글 삭제 API <http://www.tistory.com/guide/api/blog.php#comment-delete>`_ 를 통해
살펴보실 수 있습니다.

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure()

  response = pytistory.comment.delete(4,
                                    8176976,
                                    blog_name='oauth')

삭제 기능이므로, 게시글 id (``post_id``\)와 댓글 id (``comment_id``\), 블로그 명(``blog_name``\)을 전달해줍니다.

결과값은 아래처럼 받을 수 있습니다.

.. code-block:: json

  {
    "status": "200"
  }

