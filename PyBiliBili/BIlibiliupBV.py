"""
-*- coding : utf-8 -*-
获取UP投稿数据
@Author : Stupid_Cat
@Time : 2024/3/18 21:01
"""
import datetime
import json
import time
from urllib.parse import urlencode

import requests
from retrying import retry

import DefaulString
import encrtpy
import string_format


# 解析ifno
def analysis_parms(info_json):
    lis = info_json.get("data",{}).get("list",{}).get("vlist",[])
    now_count = int(info_json.get("data",{}).get("page",{}).get("pn"))*int(info_json.get("data",{}).get("page",{}).get("ps"))
    all_count = int(info_json.get("data",{}).get("page",{}).get("count"))
    has_more = True if now_count<=all_count else False
    lis_dic_ifno = []
    for each in lis:
        dic_info = dict()
        dic_info["play_num"] = each.get("play","")
        dic_info["like_num"] = each.get("photo","")
        dic_info["vid"] = each.get("aid","")
        dic_info["comment_num"] = each.get("comment","")
        dic_info["url"] = "https://www.bilibili.com/video/{}".format(each.get("bvid",""))
        dic_info["title"] = each.get("title","")
        duration, duration_str = string_format.unify_duration_format(each.get("length", ""))
        dic_info["duration"] = duration_str
        dic_info["cover"] = each.get("pic","")
        dic_info["uid"] = each.get("mid","")
        dic_info["author_name"] = each.get("author","")
        dic_info["author_url"] = "https://space.bilibili.com/{}".format(each.get("mid",""))
        dic_info["pubtime"] = each.get("created","")
        dic_info["bvid"] = each.get("bvid","")
        if dic_info["pubtime"]:
            dic_info["pubtime"] = datetime.datetime.fromtimestamp(int(str(dic_info["pubtime"])[:10])).strftime("%Y-%m-%d %H:%M:%S")
        dic_info["photoUrl"] = each.get("pic","") # 这个是默认的播放的地址 完整版的
        lis_dic_ifno.append(dic_info)
    return lis_dic_ifno,has_more

# 通过链接获取对应的信息
@retry(stop_max_attempt_number=9, wait_fixed=20)
def get_home_page_json(userId="", pcursor=1, keyword=""):

    api = 'https://api.bilibili.com/x/space/wbi/arc/search'
    dm_img_list = []
    dm_img_list = json.dumps(dm_img_list, separators=(',', ':'))

    params = DefaulString.USER_HOME_PAGEW_PARAM
    params["dm_cover_img_str"] = encrtpy.get_dm_cover_img_str()
    params["dm_img_list"] = dm_img_list
    params["mid"] = userId
    params["pn"] = pcursor
    params["wts"] = str(int(time.time()))
    cookies = DefaulString.COOKITES

    w_rid = encrtpy.calculate_md5(urlencode(params) + DefaulString.SALT)
    params['w_rid'] = w_rid
    h = DefaulString.DEFAULT_HEADERS
    h.update({'referer': f'https://m.bilibili.com/space/{userId}'})

    res = requests.get(
        api,
        headers=h,
        params=params,
        cookies=cookies,
        proxies={},
        timeout=15,
    )
    if '风控校验失败' in res.text:
        print('retrying...')
        raise

    return res.json()



# 主要的执行的函数
def get_up_video_data(userId="",pcursor=1,max_list_page=1,last_list=None,keyword=""):
    """
    userId 用户ID
    pcursor 起始页
    max_list_page 截止页
    keyword 搜索关键词 默认空
    """

    if last_list is None:
        last_list = []
    try:
        ever_page_info = get_home_page_json(userId=userId,pcursor=pcursor,keyword=keyword)
        lis_dic_ifno,has_more = analysis_parms(ever_page_info)
        last_list.extend(lis_dic_ifno)
        # print(pcursor,has_more)
        if pcursor<max_list_page and has_more :
            pcursor+=1
            return get_up_video_data(userId=userId,pcursor=pcursor,max_list_page=max_list_page,last_list=last_list,keyword=keyword)
    except Exception as e:
        return last_list
    return last_list


