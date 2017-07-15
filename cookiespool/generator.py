from cookiespool.settings import *
from cookiespool.Redis import CookiesRedisclient,AccountRedisclient
from cookiespool.tool import Captcha_By_Hand
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from PIL import Image


class CookiesGenerator(object):
    def __init__(self,name='default'):
        self.name = name
        self.cookies_db = CookiesRedisclient(name=self.name)
        self.account_db = AccountRedisclient(name=self.name)

    def get_new_cookis(self,username,password):
        raise NotImplementedError

    def set_cookies(self,account):
        result = self.get_new_cookis(account.get('username'), account.get('password'))
        if result:
            username, cookie = result
            self.cookies_db.set(username, cookie)

    def run(self):
        """主启动函数"""
        all_cookies = list(self.cookies_db.all())
        accounts = self.account_db.all()
        accounts = list(accounts)
        exist_username = [x.get('username') for x in all_cookies]
        if len(accounts):
            for account in accounts:
                if not account.get('username') in exist_username:
                    print('获取cookie:'+account.get('username'))
                    self.set_cookies(account)
        else:
            print('账号为空，不进行cookies生成')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self,name='weibo',browser_type=DEFAULT_BROWSER):
        CookiesGenerator.__init__(self, name)
        #初始化浏览器
        self.browser_type = browser_type
        if self.browser_type == 'PhantomJS':
            pass
        elif self.browser_type =='Chrome':
            self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)

    def _login_isok(self,username):
        """判断是否登录成功"""
        try:
            sign = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.me_name')))
            if sign:
                cookie_list = self.browser.get_cookies()
                cookies = {}
                for cookie in cookie_list:
                    cookies[cookie['name']] = cookie['value']
                return (username, cookies)
        except TimeoutException:
            return

    def get_new_cookis(self,username,password):
        """cookie 获取函数"""
        try:
            self.browser.delete_all_cookies()
            self.browser.get('http://my.sina.com.cn/profile/unlogin')
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'hd_login')))
            login_button.click()
            username_window = self.wait.until(EC.visibility_of_element_located((By.NAME, 'loginname')))
            username_window.send_keys(username)
            password_window = self.wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
            password_window.send_keys(password)
            button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.login_btn')))
            button.click()
            result = self._login_isok(username)
            if result:
                return result
            # 加了一个手动识别验证码的弹窗，只由于少量cookies测试时。
            print('需要验证码')
            captcha_img = self.wait(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.yzm')))
            self.browser.save_screenshot('yzm.png')
            img = Image.open('yzm.png')
            img.show()
            s = Captcha_By_Hand()
            s.run(img=img)
            print(s.captcha)
        except:
            print('登录错误，可能次数过多，被限制登录')




if __name__ == '__main__':
    pass
