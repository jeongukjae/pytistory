# -*- coding: utf8 -*-
"""PyTistory CLI 기능 구현하는 모듈입니다.
"""
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(prog='pytistory', description="Tistory Blog API Client")

    parser.add_argument('--headless', help="Headless 브라우저를 이용해 설정합니다.", action="store_true")
    parser.add_argument('--id', help="티스토리 아이디 (Headless 옵션에서 사용합니다.)")
    parser.add_argument('--password', help="티스토리 패스워드 (실행 후 입력합니다, Headless 옵션에서 사용합니다.)")
    parser.add_argument('--client_id', help="티스토리 오픈 API Client ID (Headless 옵션에서 사용합니다.)")
    parser.add_argument('--access_token', help="티스토리 오픈 API Access Token (Headless 옵션에서 사용합니다.)")

    subparsers = parser.add_subparsers(dest='kind', help='commands')
    subparsers.required = True

    # blog
    blog_parser = subparsers.add_parser('blog', help='Blog API Client')
    blog_parser.add_argument('action', choices=['info'], type=str)

    # post
    post_parser = subparsers.add_parser('post', help='Post API Client')
    post_parser.add_argument('action', choices=['list', 'write', 'modify',\
        'read', 'attach', 'delete'], type=str)

    # category
    category_parser = subparsers.add_parser('category', help='Category API Client')
    category_parser.add_argument('action', choices=['list'], type=str)

    # comment
    comment_parser = subparsers.add_parser('comment', help='Comment API Client')
    comment_parser.add_argument('action', choices=['list', 'write', 'modify',\
        'newest', 'delete'], type=str)

    # guestbook
    guestbook_parser = subparsers.add_parser('guestbook', help='Guestbook API Client')
    guestbook_parser.add_argument('action', choices=['list', 'write', 'modify', 'delete'], type=str)

    return parser.parse_args()
