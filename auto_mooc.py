# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Title: 中国大学 Mooc 自动互评脚本
# @Date: 2020/10/30
# @Author: Koorye
import selenium.webdriver
import time


class Window:
    def __init__(self):
        self.driver = selenium.webdriver.Chrome(executable_path='C://environment//chromedriver.exe')
        self.username = ''  # 填入用户名
        self.password = ''  # 填入密码
        self.evaluate_num = 5
        self.url = 'https://www.icourse163.org/member/login.htm#/webLoginIndex'

        self.driver.get(url=self.url)

    def login(self):
        self.driver.find_element_by_class_name('ux-login-set-scan-code_ft_back').click()
        self.driver.find_element_by_xpath('//ul[@class="ux-tabs-underline_hd"]/li[2]').click()
        time.sleep(15)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/iframe'))
        time.sleep(0.5)
        self.driver.find_element_by_class_name('j-nameforslide').send_keys(self.username)
        self.driver.find_element_by_class_name('j-inputtext').send_keys(self.password)
        self.driver.find_element_by_id('submitBtn').click()

    def evaluate_mooc(self):
        radio_groups = self.driver.find_elements_by_class_name('s')
        textareas = self.driver.find_elements_by_class_name('j-textarea')

        for radio_group in radio_groups:
            radios = radio_group.find_elements_by_class_name('d')
            radios[-1].find_element_by_class_name('j-select').click()

        for textarea in textareas:
            textarea.send_keys('好')

        time.sleep(0.5)
        self.driver.find_element_by_class_name('j-submitbtn').click()

    def evaluate_mooc_self(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        print("[INFO] >>> 正在进行自评")
        time.sleep(5)
        self.driver.refresh()
        time.sleep(5)
        self.driver.find_element_by_class_name('j-selfevabtn').click()
        time.sleep(5)
        self.evaluate_mooc()
        print("[INFO] >>> 自评完成")
        self.driver.refresh()

    def evaluate_mooc_repeat(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        for i in range(self.evaluate_num):
            print('[INFO] >>> 正在进行第 {} 份作业互评'.format(i + 1))
            time.sleep(5)
            self.driver.refresh()
            time.sleep(5)
            try:
                self.driver.find_element_by_xpath('//a[text()="继续进行互评"]').click()
            except Exception:
                self.driver.find_element_by_class_name('u-btn-primary').click()
            time.sleep(5)
            self.evaluate_mooc()
            print('[INFO] >>> 第 {} 份作业互评完成'.format(i + 1))
        self.driver.refresh()


if __name__ == '__main__':
    window = Window()
    window.login()
    input('输入任意内容继续：')
    window.evaluate_mooc_repeat()
    window.evaluate_mooc_self()
