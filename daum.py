# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
import csv
import colormath
import matplotlib
import numpy as np
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colorthief import ColorThief

import urllib
import os
import re



# csv 파일 읽어서 그래프 시각화
def read_csv():
    # 한글 폰트 깨짐 해결

    print(matplotlib.rcParams["font.family"])
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)

    result_csv = pd.read_csv("test.csv")
    voca_unique = pd.unique(result_csv["감성어휘"])
    print(voca_unique)

    # zero행렬 이용
    zero = np.zeros((len(result_csv), len(voca_unique)))

    # zero행렬을 DataFrame으로 변환
    dummy = pd.DataFrame(zero, columns=voca_unique)

    # 더미행렬 -> 희소행렬
    for n in enumerate(result_csv["감성어휘"]):
        dummy.ix[n] = 1

    # Term Document Matrix형식으로 변경
    TDM = dummy.T
    print(TDM)
    word_counter = TDM.sum(axis=1)  # 행 단위 합계
    print("word_counter: ", word_counter)

    # 빈도수 시각화하기
    # word_counter.plot(kind='barh', title='voca counter')

    # 내림차순 정렬
    word_counter.sort_values().plot(kind='barh', title='voca counter')
    plt.show()
    plt.savefig('test.png')


    # 썸네일 대표 색
def dominant_color_from_url(url, tmp_file='tmp.jpg'):
    '''Downloads ths image file and analyzes the dominant color'''
    urlretrieve(url, tmp_file)
    color_thief = ColorThief(tmp_file)
    dominant_color = color_thief.get_color(quality=1)
    os.remove(tmp_file)
    return dominant_color


# 썸네일 색을 가장 비슷한 KS색으로 바꿔줌
def ks_color(webtoon_color):
    red = sRGBColor(255, 0, 0)
    orange = sRGBColor(255, 127, 0)
    yellow = sRGBColor(255, 212, 0)
    yellow_green = sRGBColor(129, 193, 71)
    green = sRGBColor(0, 128, 0)
    blue_green = sRGBColor(0, 86, 102)
    blue = sRGBColor(0, 103, 163)
    blue_violet = sRGBColor(75, 0, 130)
    purple = sRGBColor(139, 0, 255)
    reddish_purple = sRGBColor(102, 0, 153)
    pink = sRGBColor(255, 51, 153)
    brown = sRGBColor(150, 75, 0)

    white = sRGBColor(255, 255, 255)
    gray = sRGBColor(128, 128, 128)
    black = sRGBColor(0, 0, 0)
    color_list = ["red", "orange", "yellow", "yellow_green", "green", "blue_green", "blue", "blue_violet",
                  "purple", "reddish_purple", "pink", "brown", "white", "gray", "black"]
    ks_list = [red, orange, yellow, yellow_green, green, blue_green, blue, blue_violet,
               purple, reddish_purple, pink, brown, white, gray, black]

    # ks_list.append(red, orange, yellow, yellow_green, green, blue_green, blue, blue_violet,
    #                purple, reddish_purple, pink, brown, white, gray, black)
    result_color = ""
    result = (-1)

    for i in range(0, len(ks_list)):
        lab_webtoon_color = convert_color(webtoon_color, LabColor)
        lab_ks_color = convert_color(ks_list[i], LabColor)
        if result == (-1):
            result = colormath.color_diff.delta_e_cie2000(lab_webtoon_color, lab_ks_color, 1, 1, 1)
            print("result: ", result)
            result_color = color_list[i]

        else:
            if result < colormath.color_diff.delta_e_cie2000(lab_webtoon_color, lab_ks_color, 1, 1, 1):
                result = colormath.color_diff.delta_e_cie2000(lab_webtoon_color, lab_ks_color, 1, 1, 1)
                result_color = color_list[i]

    print("result_color: ", result_color)
    print("final_result: ", result)
    return result_color


def remove_blanks(a_list):
    new_list = []
    for item in a_list:
        if item != "" and item != "\n":
            new_list.append(item)
    return new_list


# 감성 어휘 단색과 썸네일 단색 비교 후 감성 어휘 판단
# 감성 어휘 단색 데이터 - http://colorbank.ewha.ac.kr/colorbank/sub03_03_01.php
def sensitive_voca(thumbnail):
    temp_list = []
    f = open('voca_rgb3.csv', 'r')
    while True:
        v = f.readline()
        if v == "":
            break
        v = v.replace("(", "")
        v = v.replace(")", "")
        v = v.replace(" ", "")
        v = v.replace("\"", "")
        s = v.split(',')

        for i in range(2, len(s)):
            s[i] = s[i].replace("\\", "")
            s[i] = s[i].replace("n", "")
            s[i] = s[i].replace("R", "")
            s[i] = s[i].replace("G", ",")
            s[i] = s[i].replace("B", ",")
            # print("s[" , i , "]" , s[i])

        if s[0] == "":
            break
        s = remove_blanks(s)
        temp_list.append(s)

    print("temp_list:", temp_list)
    voca_name_list = []
    voca_color_list = []
    voca_kor_name_list = []

    for i in range(0, len(temp_list)):
        test_colors = []
        test_name = temp_list[i][0]
        test_kor_name = temp_list[i][1]
        test_voca = []
        test_voca_kor = []

        # RGB값 읽기
        # for j in range(0, int(len(temp_list[i][2:-1]) / 3) + 1):
        #     count = 2 + 3 * j
        #     if int(len(temp_list[i][2:-1]) / 3) == 0:
        #         break
        #     r = temp_list[i][count]
        #     g = temp_list[i][count + 1]
        #     b = temp_list[i][count + 2]
        #
        #     rgb = sRGBColor(r, g, b)
        #     test_colors.append(rgb)
        for j in range(2, len(temp_list[i])):
            v = temp_list[i][j].split(",")

            count = 2 + 3 * j
            if int(len(temp_list[i][2:-1]) / 3) == 0:
                break
            r = v[0]
            g = v[1]
            b = v[2]
            b = b.replace("\\", "")
            b = b.replace("n", "")
            # print("r: ", r)
            # print("g: ", g)
            # print("b: ", b)
            rgb = sRGBColor(r, g, b)
            test_colors.append(rgb)

        test_voca.append(test_name)
        test_voca.append(test_colors)

        voca_name_list.append(test_name)
        voca_color_list.append(test_colors)
        voca_kor_name_list.append(test_kor_name)

    voca_kor_name_hash = {voca_name_list[0]: voca_kor_name_list[0], voca_name_list[1]: voca_kor_name_list[1],
                          voca_name_list[2]: voca_kor_name_list[2], voca_name_list[3]: voca_kor_name_list[3],
                          voca_name_list[4]: voca_kor_name_list[4], voca_name_list[5]: voca_kor_name_list[5],
                          voca_name_list[6]: voca_kor_name_list[6], voca_name_list[7]: voca_kor_name_list[7],
                          voca_name_list[8]: voca_kor_name_list[0], voca_name_list[9]: voca_kor_name_list[9],
                          voca_name_list[10]: voca_kor_name_list[10]
                          }

    voca_hash = {voca_name_list[0]: voca_color_list[0], voca_name_list[1]: voca_color_list[1],
                 voca_name_list[2]: voca_color_list[2], voca_name_list[3]: voca_color_list[3],
                 voca_name_list[4]: voca_color_list[4], voca_name_list[5]: voca_color_list[5],
                 voca_name_list[6]: voca_color_list[6], voca_name_list[7]: voca_color_list[7],
                 voca_name_list[8]: voca_color_list[0], voca_name_list[9]: voca_color_list[9],
                 voca_name_list[10]: voca_color_list[10]
                 }
    print("voca_hash: ", voca_hash)
    print("voca_kor_name_hash: ", voca_kor_name_hash)
    f.close()

    result_voca = ""
    result = (-1)

    for i in range(0, len(voca_hash.keys())):
        voca = list(voca_hash.keys())[i]
        for k in range(0, len(voca_hash.get(voca))):
            lab_thumbnail_color = convert_color(thumbnail, LabColor)
            lab_sen_color = convert_color(voca_hash.get(voca)[k], LabColor)
            if result == (-1):
                result = colormath.color_diff.delta_e_cie2000(lab_thumbnail_color, lab_sen_color, 1, 1, 1)
                print("result: ", result)
                # result_voca = voca
                result_voca = voca_kor_name_hash.get(voca)

            else:
                if result < colormath.color_diff.delta_e_cie2000(lab_thumbnail_color, lab_sen_color, 1, 1, 1):
                    result = colormath.color_diff.delta_e_cie2000(lab_thumbnail_color, lab_sen_color, 1, 1, 1)
                    # result_voca = voca
                    result_voca = voca_kor_name_hash.get(voca)

    print("result_voca: ", result_voca)
    print("final_result: ", result)
    return result_voca


def get_webtoon_info(webtoon_name):
    json_url_webtoon = 'http://webtoon.daum.net/data/pc/webtoon/view/'

    json_string_webtoon = requests.get(json_url_webtoon + webtoon_name).text
    data_list_webtoon = json.loads(json_string_webtoon)

    print(data_list_webtoon['data']['webtoon']['title'])  # 웹툰 제목
    print(data_list_webtoon['data']['webtoon']['cartoon']['artists'][0]['name'])  # 웹툰 작가 이름
    print(data_list_webtoon['data']['webtoon']['introduction'])  # 웹툰 소개
    print(data_list_webtoon['data']['webtoon']['appThumbnailImage']['url'])  # 웹툰 썸네일 이미지

    # 웹툰 카테고리
    print("categories", end=" : ")
    for c in data_list_webtoon['data']['webtoon']['cartoon']['categories']:
        print(c['name'], end=" ")

    # 웹툰 장르
    print("\ngenres", end=" : ")
    for g in data_list_webtoon['data']['webtoon']['cartoon']['genres']:
        print(g['name'], end=" ")

    # 웹툰 에피소드 아이디, 제목, 이미지url
    total_episode = data_list_webtoon['data']['webtoon']['webtoonEpisodes']
    thumbnail = []
    dominant_color = []
    fout = open(webtoon_name + '.csv', 'a', encoding="utf-8")
    episode_voca_list = []
    for i in range(0, len(total_episode)):

        thumbnail.append(total_episode[i]['thumbnailImage']['url'])
        # print(total_episode[i]['title'])
        # print(total_episode[i]['thumbnailImage']['url'])
        dominant_color.append(dominant_color_from_url(thumbnail[i]))
        # print(dominant_color[i])

        temp = str(dominant_color[i])
        temp = re.sub('[()]', '', temp)

        x = temp
        x.replace(" ", "")
        a, b, c = x.split(",")

        color = sRGBColor(a, b, c)
        # print("sensitive_voca(color):", sensitive_voca(color))
        # print("ks_color() :", ks_color(color))

        episode_voca_list.append(sensitive_voca(color))

        fout.write(total_episode[i]['title'] + ',')

        fout.write('"' + data_list_webtoon['data']['webtoon']['cartoon']['artists'][0]['name'] + '",')

        fout.write('"' + str(dominant_color[i]) + '",')
        fout.write('"' + ks_color(color) + '",')
        fout.write(sensitive_voca(color) + '\n')
        # fout.write(temp + '\n')
    show_plot(episode_voca_list, webtoon_name)
    fout.close()

# 크롤링한 데이터 기반으로 그래프 시각화
def show_plot(voca_list, webtoon_name):
    # 한글 폰트 깨짐 해결
    print(matplotlib.rcParams["font.family"])
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)

    voca_unique = pd.unique(voca_list)
    print(voca_unique)

    # zero행렬 이용
    zero = np.zeros((len(voca_list), len(voca_unique)))

    # zero행렬을 DataFrame으로 변환
    dummy = pd.DataFrame(zero, columns=voca_unique)

    # 더미행렬 -> 희소행렬
    for n in enumerate(voca_list):
        dummy.ix[n] = 1

    # Term Document Matrix형식으로 변경
    TDM = dummy.T
    print(TDM)
    word_counter = TDM.sum(axis=1)  # 행 단위 합계
    print("word_counter: ", word_counter)

    # 빈도수 시각화하기
    # word_counter.plot(kind='barh', title='voca counter')

    # 내림차순 정렬
    word_counter.sort_values().plot(kind='barh', title='voca counter')

    # show()하기 전에 저장해야됨
    plt.savefig(webtoon_name + '.png')
    plt.show()



if __name__ == '__main__':
    #read_csv()
    webtoon_name = 'TimeofFuture'
    webtoon_name = 'hateLove'

    fout = open(webtoon_name + '.csv', 'w', encoding="utf-8")
    fout.write('episodeNum,writer,R,G,B,\n')
    get_webtoon_info(webtoon_name)
    fout.close()
