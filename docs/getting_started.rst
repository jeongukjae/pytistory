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

인증 정보 설정
--------------

인증 정보를 설정하는 방법에는 크게 세가지 방법이 있습니다.

파일을 통한 설정
*****************

파일을 통해 기본적으로 설정할 수 있습니다.
