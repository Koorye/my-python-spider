# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Title: 淘宝自动抢购脚本
# @Date: 2020/11/8
# @Author: Koorye
import selenium.webdriver
import datetime
import time


class Window:
    def __init__(self):
        self.driver = selenium.webdriver.Chrome(executable_path='C://environment//chromedriver.exe')
        self.url = 'https://cart.taobao.com/'
        self.driver.get(self.url)
        self.username = ''  # 填入用户名
        self.password = ''  # 填入密码
        self.purchase_time = datetime.datetime(2020, 11, 11, 0, 0, 0)
        self.circle_time = 0.2  # 单位：秒

    def login(self):
        self.driver.find_element_by_id('fm-login-id').send_keys(self.username)
        self.driver.find_element_by_id('fm-login-password').send_keys(self.password)
        time.sleep(1)
        self.driver.find_element_by_class_name('password-login').click()

    def purchase(self):
        if self.purchase_time <= datetime.datetime.now():
            self.driver.find_element_by_xpath('//label[@for="J_SelectAllCbx1"]').click()
            time.sleep(0.2)
            self.driver.find_element_by_id('J_SmallSubmit').click()
            time.sleep(2.5)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.find_element_by_class_name('go-btn').click()
            return True
        else:
            print('[INFO] >>> 未到抢购时间!')
            return False

    def purchase_loop(self):
        count = 1
        flag = False
        while not flag:
            print('[INFO] >>> 开始第 {} 次抢购！'.format(count))
            count += 1
            flag = self.purchase()
            time.sleep(self.circle_time)


if __name__ == '__main__':
    window = Window()
    window.login()
    time.sleep(5)
    window.purchase_loop()
