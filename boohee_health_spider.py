# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/9/6
# @Author: Koorye

import requests
import bs4
import tkinter as tk

url = 'http://www.boohee.com/food/search?keyword='


def get_soup(url):
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    return soup


def parse_soup(soup):
    item_list = soup.find(attrs={'class': 'food-list'})
    items = item_list.find_all(attrs={'class': 'item'})
    parse_items = []
    for item in items:
        temp_map = {'img': item.find(attrs={'class': 'img-box'}).find('a').find('img').attrs['src'].strip(),
                    'title': item.find('h4').text.strip(),
                    'desc': item.find('p').text.strip()}
        parse_items.append(temp_map)
    return parse_items


def print_list(items):
    for index, item in enumerate(items):
        print(str(index + 1) + '.', end=' ')
        print(item['title'])
        print(item['desc'])
        print(item['img'])
        print('----------')


def limit_str(str, max_num):
    if len(str) <= max_num:
        return str

    str = str[:max_num] + '...'
    return str


def get_result_list(url, key):
    result_list.delete(0, tk.END)
    url += key
    soup = get_soup(url)
    foods = parse_soup(soup)
    for index, food in enumerate(foods):
        result_list.insert(tk.END, str(index + 1) + '. ' + limit_str(food['title'], 16) + ' | ' + food['desc'])


if __name__ == '__main__':
    root = tk.Tk()
    input_box = tk.Entry(root, width=50)
    search_btn = tk.Button(root, text='Search', command=lambda: get_result_list(url, input_box.get()))
    result_list = tk.Listbox(root, width=60)

    root.geometry('600x400')

    input_box.place(x=50, y=50)
    search_btn.place(x=450, y=50)
    result_list.place(x=50, y=100)

    root.mainloop()
