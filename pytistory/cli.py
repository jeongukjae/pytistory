# -*- coding: utf8 -*-
"""PyTistory CLI 기능 구현하는 모듈입니다.
"""
import argparse
import json

from . import PyTistory
from .exceptions import OptionNotFoundError, ConfigurationError


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='pytistory', description="Tistory Blog API Client")

    subparsers = parser.add_subparsers(dest='kind', help='commands')
    subparsers.required = True

    # configure
    configure_parser = subparsers.add_parser(
        'configure', help='Configure Tistory API')

    configure_parser.add_argument(
        '--with-browser',
        help="브라우저를 이용해서 설정합니다.",
        action="store_true")
    configure_parser.add_argument('--id', help="티스토리 아이디")
    configure_parser.add_argument(
        '--password',
        help="티스토리 패스워드 (직접적인 인자로 넘기기보다 환경변수, 파일로 값을 넘기기를 권합니다.)")
    configure_parser.add_argument('--client_id', help="티스토리 오픈 API Client ID")
    configure_parser.add_argument('--credential', help="인증 관련 파일의 경로입니다.")

    # blog
    blog_parser = subparsers.add_parser('blog', help='Blog API Client')
    blog_parser.add_argument('action', choices=['info'], type=str)

    blog_parser.add_argument(
        '--with-browser',
        help="브라우저를 이용해서 설정합니다.",
        action="store_true")
    blog_parser.add_argument('--id', help="티스토리 아이디")
    blog_parser.add_argument(
        '--password',
        help="티스토리 패스워드 (직접적인 인자로 넘기기보다 환경변수, 파일로 값을 넘기기를 권합니다.)")
    blog_parser.add_argument('--client_id', help="티스토리 오픈 API Client ID")
    blog_parser.add_argument('--credential', help="인증 관련 파일의 경로입니다.")
    blog_parser.add_argument(
        '--access-token',
        help="티스토리 오픈 API Access Token")

    # post
    post_parser = subparsers.add_parser('post', help='Post API Client')
    post_parser.add_argument('action', choices=['list', 'write', 'modify',
                                                'read', 'attach', 'delete'], type=str)

    post_parser.add_argument(
        '--with-browser',
        help="브라우저를 이용해서 설정합니다.",
        action="store_true")
    post_parser.add_argument('--id', help="티스토리 아이디")
    post_parser.add_argument(
        '--password',
        help="티스토리 패스워드 (직접적인 인자로 넘기기보다 환경변수, 파일로 값을 넘기기를 권합니다.)")
    post_parser.add_argument('--client_id', help="티스토리 오픈 API Client ID")
    post_parser.add_argument('--credential', help="인증 관련 파일의 경로입니다.")
    post_parser.add_argument(
        '--access-token',
        help="티스토리 오픈 API Access Token")

    # category
    category_parser = subparsers.add_parser(
        'category', help='Category API Client')
    category_parser.add_argument('action', choices=['list'], type=str)

    # comment
    comment_parser = subparsers.add_parser(
        'comment', help='Comment API Client')
    comment_parser.add_argument('action', choices=['list', 'write', 'modify',
                                                   'newest', 'delete'], type=str)

    # guestbook
    guestbook_parser = subparsers.add_parser(
        'guestbook', help='Guestbook API Client')
    guestbook_parser.add_argument(
        'action', choices=['list', 'write', 'modify', 'delete'], type=str)

    return parser.parse_args()


def main():
    """PyTistory CLI를 시작합니다.
    """
    args = parse_arguments()

    pytistory = PyTistory()

    try:
        pytistory.configure(
            force_browser=args.with_browser,
            client_id=args.client_id,
            tistory_id=args.id,
            tistory_password=args.password,
            file_name=args.credential,
            access_token=args.access_token
        )
    except OptionNotFoundError:
        print("아무런 인증 옵션이 입력되지 않았습니다.\nPyTistory를 설정할 수 없습니다.")
        return
    except ConfigurationError as e:
        if "Cannot Sign into Tistory" in str(e):
            print("Tistory에 로그인할 수 없습니다.\n아이디와 비밀번호를 다시 확인해보세요")
        else:
            print(e)

        return

    if args.kind == 'configure':
        print(pytistory.access_token)

    else:
        result = pytistory\
            .__getattribute__(args.kind)\
            .__getattribute__(args.action)()

        print(json.dumps(result, ensure_ascii=True, indent=4))
