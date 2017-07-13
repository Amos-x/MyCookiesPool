from flask import Flask
from cookiespool.Redis import CookiesRedisclient,AccountRedisclient

app = Flask(__name__)

@app.route('/')
def home_page():
    """首页"""
    return '<h2>Welcome To My CookiesPool</h2>'

@app.route('/<name>/get')
def get(name):
    """
    随机获取cookie 
    请求网址如：/weibo/get
    """
    try:
        conn = CookiesRedisclient(name=name)
        return conn.random()
    except:
        return


@app.route('/<name>/cookies/count')
def cookies_count(name):
    """
    获取制定项目 已有cookie总数
    如：/weibo/cookies/count
    """
    conn = CookiesRedisclient(name=name)
    return conn.count()


@app.route('/<name>/accounts/count')
def account_count(name):
    """
    获取指定项目 已有账号总数
    如：/weibo/accounts/count
    """
    conn = AccountRedisclient(name=name)
    return conn.count()

