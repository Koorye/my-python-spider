# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/16
# @Author: Koorye

import requests
import bs4
import html2text
import os
import re


def create_essential_dir():
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    if not os.path.exists(md_path):
        os.makedirs(md_path)


def get_html_article(url):
    article_html = requests.get(url, headers=headers)
    article_soup = bs4.BeautifulSoup(article_html.text, 'html.parser')
    return article_soup.find('div', attrs={'id': 'content_views'})


def save_html_article(html_article_path, html_article_content):
    with open(html_article_path, 'w', encoding='utf-8') as f:
        print('---> SAVE: ' + html_article_path)
        f.write(str(html_article_content))


def transform_html2md(html_article_path, md_article_path):
    md_maker = html2text.HTML2Text()
    with open(html_article_path, 'r', encoding='utf-8') as f:
        md = md_maker.handle(f.read())
        with open(md_article_path, 'w', encoding='utf-8') as f2:
            print('---> TRANSFORM: ' + md_article_path)
            f2.write(md)


def get_article_url_dic():
    user_url = 'https://blog.csdn.net/' + user_name
    user_html = requests.get(user_url, headers=headers)
    user_soup = bs4.BeautifulSoup(user_html.text, 'html.parser')
    href_list = user_soup.find_all('a', attrs={'href': True})
    reg = r'^https://blog.csdn.net/{}/article/details/\d+$'.format(user_name)

    article_url_dic = {}
    for href in href_list:
        if re.search(reg, str(href.attrs['href'])) and href.text.strip().startswith('原创'):
            href_text = href.text.strip()
            href_text = href_text[3:].strip()
            href_text = href_text.replace('/', '')
            href_text = href_text.replace('"', '')

            if href_text.endswith('原力计划'):
                href_text = href_text[:-6]
            print('---> GET: ' + href.attrs['href'] + href_text)
            article_url_dic[href_text] = href.attrs['href']

    return article_url_dic


if __name__ == '__main__':
    html_path = 'csdn/html/'
    md_path = 'csdn/md/'
    user_name = 'weixin_45901207'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                             '537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'}
    dic = get_article_url_dic()

    create_essential_dir()

    for key, value in dic.items():
        html_save_path = html_path.strip() + key.strip() + '.html'
        md_save_path = md_path.strip() + key.strip() + '.md'

        html = get_html_article(value)
        save_html_article(html_save_path, get_html_article(value))
        transform_html2md(html_save_path, md_save_path)
