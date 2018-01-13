# -*- coding: utf-8 -*-
from urllib.request import urlretrieve

import colormath
import requests
import json
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colorthief import ColorThief
import urllib
import os
import re


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


# 감성 어휘 단색과 썸네일 단색 비교 후 감성 어휘 판단
# 감성 어휘 단색 데이터 - http://colorbank.ewha.ac.kr/colorbank/sub03_03_01.php
def sensitive_voca(thumbnail):
    strong = [sRGBColor(0, 119, 174), sRGBColor(0, 116, 121), sRGBColor(0, 76, 78), sRGBColor(0, 21, 29),
              sRGBColor(0, 95, 47), sRGBColor(140, 198, 71), sRGBColor(163, 207, 98), sRGBColor(179, 211, 53),
              sRGBColor(20, 27, 19)]
    unique = [sRGBColor(0, 114, 171), sRGBColor(103, 193, 193), sRGBColor(0, 177, 177), sRGBColor(0, 169, 166),
              sRGBColor(133, 200, 190), sRGBColor(0, 147, 111), sRGBColor(226, 240, 227), sRGBColor(43, 173, 111),
              sRGBColor(173, 211, 154)]
    casual = [sRGBColor(166, 222, 243), sRGBColor(127, 211, 241), sRGBColor(95, 188, 219), sRGBColor(0, 170, 221),
              sRGBColor(0, 119, 174), sRGBColor(0, 188, 198), sRGBColor(0, 116, 121), sRGBColor(135, 209, 211),
              sRGBColor(91, 196, 192)]
    cheerful = [sRGBColor(0, 164, 217), sRGBColor(1, 136, 192), sRGBColor(0, 114, 171), sRGBColor(0, 92, 139),
                sRGBColor(0, 110, 119), sRGBColor(0, 147, 111), sRGBColor(1, 159, 98), sRGBColor(0, 161, 94),
                sRGBColor(0, 140, 67)]
    dynamic = [sRGBColor(0, 77, 157), sRGBColor(0, 130, 182), sRGBColor(0, 92, 139), sRGBColor(0, 82, 119),
               sRGBColor(0, 69, 74), sRGBColor(1, 96, 90), sRGBColor(0, 76, 72), sRGBColor(0, 53, 43),
               sRGBColor(0, 102, 75)]
    sensual = [sRGBColor(201, 233, 234), sRGBColor(173, 222, 219), sRGBColor(228, 242, 231), sRGBColor(164, 217, 207),
               sRGBColor(216, 237, 221), sRGBColor(227, 234, 224), sRGBColor(160, 211, 156), sRGBColor(184, 221, 176),
               sRGBColor(235, 243, 216)]

    # sensitive_color = [strong, unique, casual, cheerful, dynamic, sensual]
    sensitive_color = {'strong': strong, 'unique': unique, 'casual': casual, 'cheerful': cheerful,
                       'dynamic': dynamic, 'sensual': sensual}

    print(sensitive_color.get('strong'))
    print(list(sensitive_color.keys())[1])
    print(sensitive_color.get('unique'))
    print(sensitive_color.get('casual'))

    sensitive_voca = ["strong", "unique", "casual", "cheerful", "dynamic", "sensual"]

    result_voca = ""
    result = (-1)

    for i in range(0, len(sensitive_color.keys())):
        voca = list(sensitive_color.keys())[i]
        for k in range(0, len(sensitive_color.get(voca))):
            lab_thumbnail_color = convert_color(thumbnail, LabColor)
            lab_sen_color = convert_color(sensitive_color.get(voca)[k], LabColor)
            if result == (-1):
                result = colormath.color_diff.delta_e_cie2000(lab_thumbnail_color, lab_sen_color, 1, 1, 1)
                print("result: ", result)
                result_voca = voca

            else:
                if result < colormath.color_diff.delta_e_cie2000(lab_thumbnail_color, lab_sen_color, 1, 1, 1):
                    result = colormath.color_diff.delta_e_cie2000(lab_thumbnail_color, lab_sen_color, 1, 1, 1)
                    result_voca = voca

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
    for i in range(0, len(total_episode)):
        thumbnail.append(total_episode[i]['thumbnailImage']['url'])
        print(total_episode[i]['title'])
        print(total_episode[i]['thumbnailImage']['url'])
        dominant_color.append(dominant_color_from_url(thumbnail[i]))
        print(dominant_color[i])

        temp = str(dominant_color[i])
        temp = re.sub('[()]', '', temp)

        x = temp
        x.replace(" ", "")
        print(temp)
        print(x.replace(" ", ""))
        a, b, c = x.split(",")
        print(a)
        print(b)
        print(c)
        color = sRGBColor(a, b, c)
        print(color)
        print("sensitive_voca(color):", sensitive_voca(color))
        print("ks_color() :", ks_color(color))

        fout.write(total_episode[i]['title'] + ',')

        fout.write('"' + data_list_webtoon['data']['webtoon']['cartoon']['artists'][0]['name'] + '",')

        # fout.write(str(dominant_color[i]) + '\n')
        fout.write(temp + '\n')
    fout.close()


if __name__ == '__main__':
    webtoon_name = 'TimeofFuture'
    fout = open(webtoon_name + '.csv', 'w', encoding="utf-8")
    fout.write('episodeNum,writer,R,G,B,\n')
    get_webtoon_info(webtoon_name)
    fout.close()
