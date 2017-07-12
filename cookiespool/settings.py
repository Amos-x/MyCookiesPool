# 是否开启web_api接口
WEB_API_ENABLED = False

# Redis数据库信息
REDIS_HOST = 'localhost'
# Redis数据库端口
REDIS_PORT = 6379
# Redis 密码
REDIS_PASSWORD = 'wyx379833553'
# 配置信息，无需修改
REDIS_DOMAIN = '*'
REDIS_NAME = '*'

# cookie生成器默认使用的浏览器
DEFAULT_BROWSER = 'Chrome'

# cookie测试周期
TEST_CYCLE = 300
# cookie 生成器检查周期（但有账号添加或删除时即账号与cookies不对应时触发生成器）
GENERATOR_CYCLE = 1600

# Cookies 生成器，格式为： name : classname
COOKIES_GENERATOR = {
    'weibo':'WeiboCookiesGenerator'
}

# Cookies 测试器,格式同上： name: classname
COOKIES_TESTER = {
    'weibo':'WeiboCookiesTester'
}