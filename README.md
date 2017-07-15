 Cookies Pool

利用redis数据库维护的一个cookies池，实现账号的模拟登录，获取cookies，异步检测cookie是否可用并更新cookie
利用Flask作为web_api，便于远程获取cookie，方便使用cookies池。（可自行添加所需功能）
可自行添加 generator.py中的cookie生成器，同时实现多个网站的模拟登录，获取cookies (目前还没添加验证码验证模块和方案，之后再完善补充)
可自信添加 tester.py中的cookie检测器，同时实现对多个网站cookie的检测

使用方法：
根据自己需求，修改 settings.py 配置文件:
然后运行 run.py 即可
设置内容：
## 是否开启web_api接口
WEB_API_ENABLED = True

## Redis数据库信息
REDIS_HOST = 'localhost'
## Redis数据库端口
REDIS_PORT = 6379
# Redis 密码 ，没有请填 None
REDIS_PASSWORD = 'xxxxxxxx'
## 基础配置信息，无需修改
REDIS_DOMAIN = '*'
REDIS_NAME = '*'

## cookie生成器默认使用的浏览器
DEFAULT_BROWSER = 'Chrome'

## cookie测试周期
TEST_CYCLE = 300
## cookie 生成器检查周期（当有账号添加或删除时即账号与cookies不对应时触发生成器）
GENERATOR_CYCLE = 1600

## Cookies 生成器，格式为： name : classname
## 注释掉即不开启生成器
COOKIES_GENERATOR = {
    'weibo':'WeiboCookiesGenerator'
}

## Cookies 测试器,格式同上： name: classname
## 注释掉即不开启检测器
COOKIES_TESTER = {
    'weibo':'WeiboCookiesTester'
}
