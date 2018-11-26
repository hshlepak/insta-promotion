from selenium.common.exceptions import WebDriverException


class LoginException(WebDriverException):
    pass


class BotLaunchException(IndexError):
    pass


class BlockedBotException(Exception):
    pass
