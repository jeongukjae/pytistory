# -*- coding: utf8 -*-
"""pytistory에서 사용되는 Exception들입니다.
"""
class ConfigurationError(Exception):
    """설정이 올바르지 않거나, 설정에 실패했을 때 일어나는 Exception입니다.
    """
    pass

class CallbackServerError(Exception):
    """CallbackServer에서 일어나는 Exception입니다. access_token을 받아오지 못하면 일어납니다.
    """
    pass
