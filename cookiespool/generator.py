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
            self.browser.quit()
        else:
            print('账号为空，不进行cookies生成')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self,name='weibo',browser_type=DEFAULT_BROWSER):
        CookiesGenerator.__init__(self, name)
        # 加了一个手动识别验证码的弹窗，只由于少量cookies测试时。
        self.captcha_deal = Captcha_By_Hand()
        #初始化浏览器
        self.browser_type = browser_type
        if self.browser_type == 'PhantomJS':
            service_args = ['--debug=[true]','--disk-cache=[true]']
            self.browser = webdriver.PhantomJS()
            self.browser.maximize_window()
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

    def _get_captcha(self):
        error_msg = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.login_error_tips')))
        if error_msg.text == '请输入验证码':
            captcha_img = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.yzm')))
            self.browser.save_screenshot('../captcha_image/web.png')
            img = Image.open('web.png')
            im = img.crop((440, 450, 530, 490))  # 这里输入验证码的坐标区域进行截图剪裁，原有的是随意填写的，以实际情况为准。
            im.save('../captcha_image/captcha.png')
            self.captcha_deal.run(im)
            return self.captcha_deal.captcha
        else:
            print(error_msg.text)
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
            captcha = self._get_captcha()
            # 由于本人并没实际使用多帐号进行测试，始终没有模拟出让我输入验证码的情况，
            # 所以下面的验证码输入窗口，没法捕获，请使用者根据实际情况自行完善。
            if captcha:
                captcha_input = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '自行填写')))
                captcha_input.send_keys(captcha)
                button.click()
                return self._login_isok(username)
            else:
                return
        except:
            print('获取验证码出错')
            return


if __name__ == '__main__':
    s = WeiboCookiesGenerator()
    s.run()
