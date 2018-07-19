Category API
============

Category 리스트 조회
--------------------

카테고리 목록을 가져올 수 있는 API입니다. 해당 API에 관한 정보는
`카테고리 리스트 조회 API <http://www.tistory.com/guide/api/blog.php#category-list>`_ 를 통해
살펴보실 수 있습니다.

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure()

  response = pytistory.category.list(blog_name='oauth')

결과값은 아래처럼 받을 수 있습니다.

.. code-block:: json

  {
    "status": "200",
    "item": {
      "url": "oauth",
      "secondaryUrl": "",
      "categories": {
        "category": [
          {
            "id": "403929",
            "name": "OAuth2.0 Athentication",
            "parent": "",
            "label": "OAuth2.0 Athentication",
            "entries": "0"
          },
          {
            "id": "403930",
            "name": "Blog API Series",
            "parent": "",
            "label": "Blog API Series",
            "entries": "0"
          },
          {
            "id": "403931",
            "name": "Post API Series",
            "parent": "",
            "label": "Post API Series",
            "entries": "0"
          },
          {
            "id": "403932",
            "name": "Category API Series",
            "parent": "",
            "label": "Category API Series",
            "entries": "0"
          },
          {
            "id": "403933",
            "name": "Comment API Series",
            "parent": "",
            "label": "Comment API Series",
            "entries": "0"
          },
          {
            "id": "403934",
            "name": "Guestbook API Series",
            "parent": "",
            "label": "Guestbook API Series",
            "entries": "0"
          }
        ]
      }
    }
  }

