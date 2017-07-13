from cookiespool.settings import *
from cookiespool.generator import *
from cookiespool.tester import *
from cookiespool.web_api import app
from multiprocessing import Process
import time

class Scheduler(object):
    @staticmethod
    def test_cookies(test_cycle=TEST_CYCLE):
        while True:
            try:
                for name, classname in COOKIES_TESTER.items():
                    print(classname +'循环检测器启动')
                    tester = eval(classname + '(name="'+name+'")')
                    tester.run()
                    del tester
                print('检测完成，睡眠一个周期')
                time.sleep(test_cycle)
            except:
                print('循环检测器 错误')

    @staticmethod
    def cookie_generator(generator_cycle = GENERATOR_CYCLE):
        while True:
            try:
                for name,classname in COOKIES_GENERATOR.items():
                    print(classname +'循环生成器启动')
                    generator = eval(classname + '(name="'+name+'")')
                    generator.run()
                    del generator
                print('生成cookies完成，睡眠一个周期')
                time.sleep(generator_cycle)
            except:
                print('循环生成器 错误')

    def run(self):
        try:
            if COOKIES_GENERATOR:
                process_generator = Process(target=Scheduler.cookie_generator)
                process_generator.start()
        except:
            print('Cookies生成器为空或未开启')

        try:
            if COOKIES_TESTER:
                process_test = Process(target=Scheduler.test_cookies)
                process_test.start()
        except:
            print('Cookies检测器为空或未开启')

        if WEB_API_ENABLED:
            app.run()

if __name__ == '__main__':
    r = Scheduler()
    r.run()