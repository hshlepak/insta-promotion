from selenium.common.exceptions import WebDriverException


class LoginException(WebDriverException):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class BotLaunchException(IndexError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class BlockedBotException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
