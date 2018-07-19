# -*- coding: utf8 -*-
"""pytistory에서 사용되는 Exception들입니다.
"""


class ConfigurationError(Exception):
    """설정이 올바르지 않거나, 설정에 실패했을 때 일어나는 Exception입니다.
    """
    pass


class InvalidSectionError(ConfigurationError):
    """Tistory 인증 정보가 담긴 파일을 파싱하며, 올바른 섹션을 찾을 수 없을 때
    일어나는 Exception입니다.
    """
    pass


class InvalidNameError(ConfigurationError):
    """Tistory 인증 정보가 담긴 파일을 파싱하며, 올바른 Name을 찾을 수 없을 때
    일어나는 Exception입니다.
    """
    pass


class InvalidAccountError(ConfigurationError):
    """Tistory 로그인을 올바르지 않은 계정 정보일 때 일어나는 Exception입니다.
    """
    pass


class EmailAuthError(ConfigurationError):
    """Tistory 로그인을 하면서 이메일 인증이 발생할 때 일어나는 Exception입니다.
    """
    pass


class WebDriverError(ConfigurationError):
    """Tistory 인증 중 Headless Chrome을 사용할 수 없어 일어나는 에러입니다.
    """
    pass


class TokenNotFoundError(ConfigurationError):
    """Tistory 인증 마지막 과정에서 토큰을 찾을 수 없을 때,
    또는 API 실행 중 토큰이 설정되어 있지 않을 때 일어나는 에러입니다.
    """
    pass


class OptionNotFoundError(ConfigurationError):
    """인증과정에서 아무런 설정 옵션을 찾을 수 없을 때 일어나는 에러입니다.
    """
    pass


class ParsingError(Exception):
    """Tistory API를 사용하며 적절한 응답이 오지 않을 때 일어나는 Exception입니다.
    """
    pass

class JSONDecodingError(Exception):
    """Tistory API를 사용할 때 적절한 JSON 문자가 오지 않을 때 일어나는 에러입니다.
    """
    pass

class NoSpecifiedBlogError(Exception):
    """명시된 블로그가 없을때 일어나는 에러입니다.
    """
    pass
