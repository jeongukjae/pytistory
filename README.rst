PyTistory
=========

.. image:: https://circleci.com/gh/JeongUkJae/pytistory.svg?style=shield
  :target: https://circleci.com/gh/JeongUkJae/pytistory
.. image:: https://travis-ci.org/JeongUkJae/pytistory.svg?branch=master
  :target: https://travis-ci.org/JeongUkJae/pytistory
.. image:: https://codecov.io/gh/JeongUkJae/pytistory/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/JeongUkJae/pytistory
.. image:: https://requires.io/github/JeongUkJae/pytistory/requirements.svg?branch=master
  :target: https://requires.io/github/JeongUkJae/pytistory/requirements/?branch=master
.. image:: https://img.shields.io/pypi/v/pytistory.svg
  :target: https://pypi.org/project/pytistory
.. image:: https://img.shields.io/pypi/pyversions/pytistory.svg
  :target: https://pypi.org/project/pytistory
.. image:: https://img.shields.io/pypi/l/pytistory.svg
  :target: https://pypi.org/project/pytistory
.. image:: https://img.shields.io/pypi/status/pytistory.svg
  :target: https://pypi.org/project/pytistory

PyTistory는 `티스토리 오픈 API 가이드 <http://www.tistory.com/guide/api/index>`_ 를 참고하여 Python으로 작성한 티스토리
API 클라이언트입니다. `티스토리 오픈 API 가이드 인증 방식 <http://www.tistory.com/guide/api/oauth>`_ 중
Client-side flow 방식에 따라 구현되었습니다.

Installation
------------

pytistory는 ``pip``\ 를 통해 설치할 수 있습니다.

.. code-block:: bash

   $ pip install pytistory


사용법
-------

사용자 인증
~~~~~~~~~~~

인증정보는 다음과 같은 우선순위를 통해 적용됩니다.

  - 직접 설정하는 ``configure``\ 함수로 넘어오는 ``access_token``\인자값
  - ``configure``\ 함수로 넘어오는 ``client_id``\, ``tistory_id``\, ``tistory_password``\ 인자값
  - ``configure``\ 함수로 넘어오는 ``file_name``\에서 읽어들인 인자값
  - 환경변수값
  - 기본 파일(``~/.pytistory/credentials.ini``\)에 설정되어 있는 값

즉, 환경변수, 기본 설정 파일에 client id가 적용되어 있다 하더라도 직접 넘기는 ``file_name``\에 존재하는 설정들에 의해 덮어씌워지고,
직접 인자값으로 넘기는 ``client_id``\등의 인자값에 의해 덮어씌워집니다.

``access_token``\이 인자로 넘어올 경우 다른 옵션은 전부 무시하고, ``access_token``\만을 설정합니다.

직접 Access Token 설정
********************************

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure(
    access_token='some-example-access-token')

함수의 인자값을 통한 설정
********************************

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure(
    client_id='some-example-client-id',
    tistory_id='some-example-tistory-id',
    tistory_password='some-example-tistory-password')

파일을 통한 설정
******************

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure(
    file_name='./some/path/to/credentials.ini')

파일 형식은 ini(Initialization)을 따릅니다.

.. code-block:: ini

  [pytistory]
  client_id=some-client-id
  tistory_id=some-tistory-id
  tistory_password=some-tistory-password

환경변수를 통한 설정
**********************

환경 변수로는 다음과 같이 설정할 수 있습니다.

.. code-block:: bash

  export PYTISTORY_CLIENT_ID=some-example-client-id
  export PYTISTORY_TISTORY_ID=some-example-tistory-id
  export PYTISTORY_TISTORY_PASSWORD=some-example-tistory-password


작성 중

기여
----

이 프로젝트는 부족한 점이 많습니다. Contribution은 언제나 환영입니다. 혹시 오류, 버그 혹은 업데이트가 필요한 점이 있으시다면
`PR <https://github.com/JeongUkJae/pytistory/pulls>`_ 또는 `Issue <https://github.com/JeongUkJae/pytistory/issues>`_ 를 통해
언제든지 알려주세요. 👏

Copyright & License
-------------------

Copyright (c) 2018 JeongUkJae. MIT License.
