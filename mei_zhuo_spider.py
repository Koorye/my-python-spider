# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/14
# @Author: Koorye

import requests
import bs4
import xpinyin
import os


def get_html(url):
    """ Get html from url with headers. """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
                             '537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    return requests.get(url, headers=headers)


def get_pinyin(word):
    """ Transform Chinese words into plain pinyin. """
    my_pinyin = xpinyin.Pinyin()
    original_pinyin = my_pinyin.get_pinyin(word)
    pinyin_list = original_pinyin.split('-')
    result = ''
    for word in pinyin_list:
        result += word
    return result


def save_img(url, img_path, save_path):
    """ Save image from url to designated path. """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    resp = requests.get(url)
    if os.path.exists(save_path + img_path):
        print("保存失败！文件已存在：{}".format(img_path))
    else:
        with open(save_path + img_path, 'wb') as f:
            f.write(resp.content)
            f.close()


def get_img_path(req_html):
    """ Parse html, then get image href and text. """
    print("访问的页面：{}，当前目录：第{}页".format(str(req_html.url), index))
    soup = bs4.BeautifulSoup(req_html.text, 'html.parser', from_encoding='utf-8')
    resp_list = soup.find_all('a')
    resp_index = 1
    for resp in resp_list:
        if resp.find('img') and resp.find('p') and 'title' not in resp.find('img').attrs:
            print('{}.\t链接：{}\t标题：{}'.format(resp_index, resp.attrs['href'], resp.find('p').text))
            resp_index += 1

            save_img(resp.find('img').attrs['data-original'], resp.find('p').text + '.png', img_save_path)
    print('--*-- 图片已保存 --*--')


if __name__ == '__main__':
    target_url = 'http://www.win4000.com/zt/'
    img_save_path = 'img/'

    index = 1
    next_page = '1'
    html = ''
    key_word = input("请输入查询的关键词（如风景）：")
    pinyin = get_pinyin(key_word)

    while get_html(target_url + pinyin + '.html').status_code != 200:  # eliminate incorrect keywords
        print("无法找到关键词对应的网页！")
        key_word = input("请输入查询的关键词（如风景）：")
        pinyin = get_pinyin(key_word)

    while True:
        # Next Page
        if next_page == 'y':  # to next page
            index += 1
            html = get_html(target_url + pinyin + '_{}.html'.format(index))

        elif next_page == 'n':  # break
            print("程序结束！")
            break

        elif next_page.isdigit():  # to designated page
            index = int(next_page)
            html = get_html(target_url + pinyin + '_{}.html'.format(next_page))

        else:  # error input
            while next_page != 'y' and next_page != 'n' and not next_page.isdigit():
                print("输入异常，请重新输入！")
                next_page = input("是否查询下一页？(y/n)，或输入数字查询指定页面：")

        # Response
        if html.status_code == 200:  # request success
            print("访问成功！")
            get_img_path(html)
            next_page = input("是否查询下一页？(y/n)，或输入数字查询指定页面：")

        elif html.status_code == 404:  # cannot find website
            print("未能找到对应的网页，请确认关键词是否正确！")
            next_page = ''
        else:
            print("未知错误！")
            next_page = ''

    os.system('chcp 65001')
    os.system('pause')
