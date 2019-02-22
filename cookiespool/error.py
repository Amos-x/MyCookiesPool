class CookiesPoolError(Exception):
    def __str__(self):
        return repr('cookies pool Error')


class SetCookiesError(CookiesPoolError):
    def __str__(self):
        return repr('set cookie Error')


class GetCookiesError(CookiesPoolError):
    def __str__(self):
        return repr('get cookie Error')


class DeleteCookiesError(CookiesPoolError):
    def __str__(self):
        return repr('delete cookie Error')


class RandomCookieError(CookiesPoolError):
    def __str__(self):
        return repr('random cookie Error')


class GetAllCookiesError(CookiesPoolError):
    def __str__(self):
        return repr('get all cookies Error')


class SetAccountError(CookiesPoolError):
    def __str__(self):
        return repr('Set Account Error')


class DeleteAccountError(CookiesPoolError):
    def __str__(self):
        return repr('Delete Account Error')


class GetAccountError(CookiesPoolError):
    def __str__(self):
        return repr('Get Account Error')


class GetAllAccountError(CookiesPoolError):
    def __str__(self):
        return repr('Get All Account Error')