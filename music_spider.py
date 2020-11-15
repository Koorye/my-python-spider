# !usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2020/6/29
# @Author: Koorye

import selenium.webdriver
import time
import requests
import os
import eyed3
import enum


class MusicWebsite(enum.Enum):
    CloudMusic = 1
    QQMusic = 2
    XiamiMusic = 3
    KugouMusic = 4
    BaiduMusic = 5


def download_mp3(download_url, download_music_name, download_author_name, download_album_name):
    if not os.path.exists('music'):
        os.makedirs('music')

    html = requests.get(download_url)
    with open('music/{}.mp3'.format(download_music_name), 'wb') as f:
        for chunk in html.iter_content():
            f.write(chunk)

    audio = eyed3.load('music/{}.mp3'.format(download_music_name))
    audio.initTag()
    audio.tag.artist = download_author_name
    audio.tag.album = download_album_name
    audio.tag.album_artist = download_author_name
    audio.tag.title = download_music_name
    audio.tag.save()

    print('[ Info ] Download success!')


def get_mp3(key_word):
    for order in download_order_list:
        driver.find_element_by_xpath('//*[@id="btn-area"]/span[4]').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="search-wd"]').clear()
        driver.find_element_by_xpath('//*[@id="search-wd"]').send_keys(key_word)  # input key word
        driver.find_element_by_xpath(
            '//*[@id="music-source"]/label[{}]/input'.format(str(order.value))).click()  # choose music website
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="search-area"]/div[1]/button').click()  # click search button
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="mCSB_2_container"]/div[2]/span[2]').click()  # click menu button
        time.sleep(0.5)
        driver.find_element_by_class_name('info-btn').click()  # open mp3 website

        time.sleep(2)
        if len(driver.window_handles) < 2:  # unable to open mp3 url
            print('[ Error ] Download denied from {}! Trying to use other source.'.format(order))
        else:
            break  # open mp3 url successfully

    driver.switch_to.window(driver.window_handles[-1])
    new_url = driver.current_url  # get mp3 url
    driver.close()  # switch to music website
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(1)
    driver.find_element_by_class_name('layui-layer-close').click()

    time.sleep(0.5)
    new_music_name = driver.find_element_by_xpath('//*[@id="mCSB_2_container"]/div[2]/span[5]/span').text
    new_author_name = driver.find_element_by_xpath('//*[@id="mCSB_2_container"]/div[2]/span[4]').text
    new_album_name = driver.find_element_by_xpath('//*[@id="mCSB_2_container"]/div[2]/span[3]').text

    print('[ Info ] Music name:' + new_music_name +
          ', Author name: ' + new_author_name + ', Album name: ' + new_album_name)
    download_mp3(new_url, new_music_name, new_author_name, new_album_name)


if __name__ == '__main__':
    url = 'http://guozhivip.com/yinyue/'
    music_list = ['夜に駆ける']
    download_order_list = [MusicWebsite.XiamiMusic, MusicWebsite.QQMusic, MusicWebsite.CloudMusic,
                           MusicWebsite.KugouMusic, MusicWebsite.BaiduMusic]
    driver = selenium.webdriver.Chrome()
    driver.set_window_size(800, 600)
    driver.get(url)

    for music in music_list:
        get_mp3(music)

    driver.quit()
