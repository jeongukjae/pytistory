시작하기
=========

설치
----

pytistory는 ``pip``\ 를 통해 설치할 수 있습니다.

.. code-block:: bash

   $ pip install pytistory


티스토리 서비스 등록
--------------------

먼저, 티스토리 API를 사용하기 위해 OAuth 과정을 거쳐야합니다. 그를 위해 티스토리 API client_id가 필요합니다.
그를 위해 `티스토리 오픈 API 인증 가이드 <http://www.tistory.com/guide/api/oauth>`_\ 에서, 클라이언트 등록을 합니다.

.. image:: _static/images/OAuth\ Registration.png

서비스 형태와 서비스 권한, Callback 경로를 적절하게 수정해야 합니다.

서비스 형태는 ``PC 애플리케이션``\ 으로, Callback 경로는 ``http://0.0.0.0:5000/callback``\ 으로 설정합니다. 서비스 권한은
사용하실만큼 설정하시면 됩니다. 하지만, ``읽기/쓰기``\ 를 권장드립니다.

사용자 인증
--------------

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure(
    access_token='some-example-access-token')

함수의 인자값을 통한 설정
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure(
    client_id='some-example-client-id',
    tistory_id='some-example-tistory-id',
    tistory_password='some-example-tistory-password')

파일을 통한 설정
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from pytistory import PyTistory

  pytistory = PyTistory()
  pytistory.configure(
    file_name='./some/path/to/credentials.ini')

파일 형식
**********

파일 형식은 ini(Initialization)을 따릅니다.

.. code-block:: ini

  [pytistory]
  client_id=some-client-id
  tistory_id=some-tistory-id
  tistory_password=some-tistory-password

환경변수를 통한 설정
~~~~~~~~~~~~~~~~~~~~~

환경 변수로는 다음과 같이 설정할 수 있습니다.

.. code-block:: bash

  export PYTISTORY_CLIENT_ID=some-example-client-id
  export PYTISTORY_TISTORY_ID=some-example-tistory-id
  export PYTISTORY_TISTORY_PASSWORD=some-example-tistory-password
