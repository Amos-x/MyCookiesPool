import redis
import random
from cookiespool.settings import *
from cookiespool.error import *


class Redisclient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        if password:
            self.client = redis.Redis(host,port,2,password)
        else:
            self.client = redis.Redis(host,port,2)

        self.domain = REDIS_DOMAIN
        self.name = REDIS_NAME

    def _key(self,key):
        return "{domain}:{name}:{key}".format(domain=self.domain,name=self.name,key=key)

    def set(self,key,value):
        raise NotImplementedError

    def get(self,key):
        raise NotImplementedError

    def delete(self,key):
        raise NotImplementedError

    def keys(self):
        return self.client.keys('{domain}:{name}:*'.format(domain=self.domain,name=self.name))

    def flush(self):
        """清空数据库"""
        self.client.flushall()


class CookiesRedisclient(Redisclient):

    def __init__(self,domain='cookies',name='default'):
        Redisclient.__init__(self)
        self.domain = domain
        self.name = name

    def set(self, key, value):
        try:
            self.client.set(self._key(key), value)
        except:
            raise SetCookiesError

    def get(self,key):
        try:
            return self.client.get(self._key(key)).decode('utf-8')
        except:
            raise GetCookiesError

    def delete(self,key):
        try:
            self.client.delete(self._key(key))
        except:
            raise DeleteCookiesError

    def random(self):
        try:
            keys = self.keys()
            return self.client.get(random.choice(keys))
        except:
            raise RandomCookieError

    def count(self):
        return len(self.keys())

    def all(self):
        try:
            for key in self.keys():
                group = key.decode('utf-8').split(':')
                if len(group) == 3:
                    username = group[2]
                    yield {
                        'username': username,
                        'password': self.get(username)
                    }
        except:
            raise GetAllCookiesError


class AccountRedisclient(Redisclient):
    def __init__(self,domain='account',name='default'):
        Redisclient.__init__(self)
        self.domain = domain
        self.name = name

    def set(self, key, value):
        try:
            self.client.set(self._key(key), value)
        except:
            raise SetAccountError

    def get(self, key):
        try:
            return self.client.get(self._key(key)).decode('utf-8')
        except:
            raise GetAccountError

    def delete(self, key):
        try:
            self.client.delete(self._key(key))
        except:
            raise DeleteAccountError

    def all(self):
        try:
            for key in self.keys():
                group = key.decode('utf-8').split(':')
                if len(group) == 3:
                    username = group[2]
                    yield {
                        'username': username,
                        'password': self.get(username)
                    }
        except:
            raise GetAllAccountError

    def count(self):
        return len(self.keys())


if __name__ == '__main__':
    s = CookiesRedisclient(name='weibo')
    print(s.keys())
    # print(s.get('username'))
    print(list(s.all()))
    if not list(s.all()):
        print('OK')