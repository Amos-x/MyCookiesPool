from cookiespool.settings import *
from cookiespool.Redis import CookiesRedisclient,AccountRedisclient
from cookiespool.generator import *
import aiohttp
import asyncio
from bs4 import BeautifulSoup


class CookiesTester(object):
    def __init__(self,name='default'):
        self.name = name
        self.cookies_db = CookiesRedisclient(name=self.name)
        self.account_db = AccountRedisclient(name=self.name)

    async def test(self,username,password):
        raise NotImplementedError

    def run(self):
        """主启动函数"""
        id_and_cookie = self.cookies_db.all()
        id_and_cookie = list(id_and_cookie)
        try:
            if id_and_cookie:
                loop = asyncio.get_event_loop()
                tasks = [self.test(x.get('username'), x.get('cookie')) for x in id_and_cookie]
                loop.run_until_complete(asyncio.wait(tasks))
                loop.close()
            else:
                print('cookies为空，睡眠一个周期')
        except:
            print('异步检测 run() 错误')


class WeiboCookiesTester(CookiesTester):
    def __init__(self,name='weibo'):
        CookiesTester.__init__(self,name)
        self.generator = WeiboCookiesGenerator(name=name)

    async def test(self, username, cookie):
        """异步检测函数"""
        try:
            password = self.account_db.get(username)
            async with aiohttp.ClientSession(cookies=eval(cookie)) as session:
                async with session.get('http://weibo.com') as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), 'lxml')
                        sign = soup.select('title')[0].get_text()
                        if not '我的首页' in sign:
                            self.cookies_db.delete(username)
                            account = {
                                'username': username,
                                'password': password
                            }
                            if account in list(self.account_db.all()):
                                self.generator._init_browser()
                                self.generator.set_cookies(account)
        except:
            print('异步检测 test() 错误')



