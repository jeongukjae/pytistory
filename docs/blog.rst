Blog API
========

Blog 정보 조회
--------------

블로그 정보를 받아오는 API입니다. 해당 API에 관한 정보는
`링크 <http://www.tistory.com/guide/api/blog.php#blog-info>`_ 를 통해
살펴보실 수 있습니다.

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure()

  response = pytistory.blog.info()

결과값은 아래처럼 받을 수 있습니다.

.. code-block:: json

  {
    "status": "200",
    "id": "blogtest_080@hanmail.net",
    "item": [
      {
        "url": "http://oauth.tistory.com",
        "secondaryUrl": "http://",
        "nickname": "Tistory API",
        "title": "나만의 앱, Tistory OAuth API 로 만들어보세요!",
        "description": "",
        "default": "Y",
        "blogIconUrl":
          "http://i1.daumcdn.net/cfs.tistory/blog/79/795307/index.gif",
        "faviconUrl":
          "http://i1.daumcdn.net/cfs.tistory/blog/79/795307/index.ico",
        "profileThumbnailImageUrl":
          "http://cfile1.uf.tistory.com/R106x0/1851DB584DAF942950AF29",
        "profileImageUrl":
          "http://cfile1.uf.tistory.com/R106x0/1851DB584DAF942950AF29",
        "statistics": {
          "post": "3",
          "comment": "0",
          "trackback": "0",
          "guestbook": "0",
          "invitation": "0"
        }
      },
      {
        "url": "http://oauth2.tistory.com",
        "secondaryUrl": "http://",
        "nickname": "Tistory API",
        "title": "나만의 비밀 홈",
        "description": "",
        "default": "N",
        "blogIconUrl":
          "http://i1.daumcdn.net/cfs.tistory/blog/79/795308/index.gif",
        "faviconUrl":
          "http://i1.daumcdn.net/cfs.tistory/blog/79/795308/index.ico",
        "profileThumbnailImageUrl": "",
        "profileImageUrl": "",
        "blogId": "795308",
        "statistics": {
          "post": "0",
          "comment": "0",
          "trackback": "0",
          "guestbook": "0",
          "invitation": "0"
        }
      }
    ]
  }

