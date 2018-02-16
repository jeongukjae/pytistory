# -*- coding: utf8 -*-
#pylint: disable=W0612
# disable the pylint message W0612 `Unused variable 'callback' and
# 'callback_modified'`
"""티스토리 OAuth 인증을 위한 로컬서버입니다.
"""
from flask import Flask, request

HASH_TO_ARGS = """
<script>
window.onload = function () {
    location.href = '/callback_modified?' + window.location.hash.substring(1);
}
</script>
"""

CLOSE_WINDOW = """
<script>
window.close()
</script>
"""

class CallbackServer:
    """티스토리 OAuth를 위해 로컬 서버를 엽니다.
    """
    def __init__(self, namespace, event):
        self.namespace = namespace
        self.event = event

    def prepare(self):
        """Flask App을 실행시킵니다.

        `GET /callback`과 `GET /callback_modified`인 두개의 라우팅을 받는데,
        첫번째 라우팅에서는 uri 뒤의 해쉬를 서버에서 파라미터로 받기 위해 다시 고쳐주는 역할만을 합니다.
        두번째 라우팅에서는 access_token을 받아 namespace에 access_token을 설정하고,
        flask app을 종료시킵니다.
        """
        app = Flask(__name__)

        @app.route('/callback')
        def callback():
            """tistory OAuth 인증 redirect_url에 해당하는 함수입니다.

            `/callback_modified`로 리다이렉션 시키는 응답을 내보냅니다.

            :return: 요청 경로 상의 해시를 GET 파라미터로 바꾸어주는 스크립트를 반환합니다.
            :rtype: str
            """
            return HASH_TO_ARGS

        @app.route('/callback_modified')
        def callback_modified():
            """access_token을 실제로 처리하는 함수입니다.

            flask app을 종료시키고, access_token을 메인 프로세스에 전달합니다.

            :return: 창을 닫아주는 스크립트를 반환합니다.
            :rtype: str
            """
            access_token = request.args.get('access_token')

            # set access token and shutdown server
            self.namespace.access_token = access_token
            self.event.set()
            self.shutdown_server()

            return CLOSE_WINDOW

        app.run(host='localhost')

    @staticmethod
    def shutdown_server():
        """flask 앱을 종료시키는 함수입니다.

        :raises RuntimeError: Flask 앱이 실행중이 아니라면 종료할 수 없습니다.
        """
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
