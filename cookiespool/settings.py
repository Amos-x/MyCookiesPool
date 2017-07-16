# 是否开启web_api接口
WEB_API_ENABLED = True

# Redis数据库信息
REDIS_HOST = 'localhost'
# Redis数据库端口
REDIS_PORT = 6379
# Redis 密码 ，没有请填 None
REDIS_PASSWORD = 'wyx379833553'
# 基础配置信息，无需修改
REDIS_DOMAIN = '*'
REDIS_NAME = '*'

# cookie生成器默认使用的浏览器
DEFAULT_BROWSER = 'PhantomJS'

# cookie测试周期
TEST_CYCLE = 300
# cookie 生成器检查周期（当有账号添加或删除时即账号与cookies不对应时触发生成器）
GENERATOR_CYCLE = 1600

# Cookies 生成器，格式为： name : classname
# 注释掉即不开启生成器
COOKIES_GENERATOR = {
    'weibo':'WeiboCookiesGenerator'
}

# Cookies 测试器,格式同上： name: classname
# 注释掉即不开启检测器
COOKIES_TESTER = {
    'weibo':'WeiboCookiesTester'
}
