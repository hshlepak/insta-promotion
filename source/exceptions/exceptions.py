from selenium.common.exceptions import WebDriverException


class LoginException(WebDriverException):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
