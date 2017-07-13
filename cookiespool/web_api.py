from flask import Flask
from cookiespool.Redis import CookiesRedisclient,AccountRedisclient

app = Flask(__name__)

@app.route('/')
def home_page():
    return '<h2>Welcome To My CookiesPool</h2>'

@app.route('/<name>/get')
def get(name):
    """请求网址如：/weibo/get"""
    try:
        conn = CookiesRedisclient(name=name)
        return conn.random()
    except:
        return


@app.route('/<name>/cookies/count')
def cookies_count(name):
    conn = CookiesRedisclient(name=name)
    return conn.count()


@app.route('/<name>/account/count')
def account_count(name):
    conn = AccountRedisclient(name=name)
    return conn.count()

