"""
-*- coding : utf-8 -*-
主要功能类
@Author : Stupid_Cat
@Time : 2024/3/16 14:54
"""

import requests
import os
from time import sleep
import json
import time
import pandas as pd
from DefaulString import DEFAULT_HEADERS
import re
import pymysql


class Spider(object):

    def __init__(self, Cookies):
        self.cookies = Cookies
        self.name = self.Cookies_name_get()

    def validateTitle(self, title):
        re_str = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(re_str, "_", title)  # 替换为下划线
        return new_title

    def intToStrTime(self, a):
        b = time.localtime(a)  # 转为日期字符串
        c = time.strftime("%Y/%m/%d %H:%M:%S", b)  # 格式化字符串
        return c

    def get_aid(self, bv):
        response = requests.get(url=f'https://www.bilibili.com/video/{bv}', headers=DEFAULT_HEADERS)
        res = re.findall('<script>window.__INITIAL_STATE__=(.*)?;\(function\(\)', response.text, re.S)

        json_data = json.loads(res[0])
        if 'message' in json_data['error']:
            print(json_data['error']['message'])
            return Exception("错误")
        aid = json_data['aid']
        return aid

    def get_title(self, bv):
        response = requests.get(url=f'https://www.bilibili.com/video/{bv}', headers=DEFAULT_HEADERS)
        res = re.findall('<script>window.__INITIAL_STATE__=(.*)?;\(function\(\)', response.text, re.S)

        json_data = json.loads(res[0])
        if 'message' in json_data['error']:
            print(json_data['error']['message'])
            return Exception("错误")
        title = json_data['videoData']['title']
        return title

    def get_response(self, aid, page=1):
        video_info_url = 'https://api.bilibili.com/x/web-interface/archive/relation?aid={}'.format(aid)

        res_json = requests.get(url=video_info_url, headers=DEFAULT_HEADERS, cookies=self.cookies).json()
        print(res_json)
        # like_count, coin_count, collection_count = res_json['data']['like'], res_json['data']['coin'], res_json['data']['favorite']
        # print(aid, title, like_count, coin_count, collection_count)

        comment_url = 'https://api.bilibili.com/x/v2/reply?callback=jQueryjsonp=jsonp&pn={}&type=1&oid={}&sort=2&_=1594459235799'

        response = requests.get(url=comment_url.format(page, aid), headers=DEFAULT_HEADERS)

        return response

    def get_Comment_tocsv(self, bvs):
        save_folder = 'Comment'
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)

        if not isinstance(bvs, list):
            ValueError("传入的类型不是list")
        if not bvs:
            ValueError("未传入正确的Bv列表")
        for bv in bvs:
            print(bv)
            aid = self.get_aid(bv)
            title = self.get_title(bv)
            title = self.validateTitle(title=title)
            response = self.get_response(aid=aid)

            total_page = json.loads(response.text)['data']['page']['count'] // 20 + 1
            page = 1
            is_root, uname, comments, times, likes = [], [], [], [], []
            while True:
                # print(response.text)
                data = json.loads(response.text)['data']['replies']
                if not data:
                    data = json.loads(response.text)['data']
                    if 'hots' in data.keys():
                        data = data['hots']
                    else:
                        break
                for row in data:
                    print('根评论', row['member']['uname'], row['content']['message'])
                    is_root.append('是')
                    times.append(self.intToStrTime(row['ctime']))
                    uname.append(row['member']['uname'])
                    comments.append(row['content']['message'])
                    likes.append(row['like'])

                    if row.get('replies'):
                        for crow in row['replies']:
                            is_root.append('否')
                            times.append(self.intToStrTime(crow['ctime']))
                            uname.append(crow['member']['uname'])
                            comments.append(crow['content']['message'])
                            likes.append(crow['like'])
                            print('---子评论', crow['member']['uname'], crow['content']['message'])

                page += 1
                if page > total_page:
                    break
                sleep(1)
                response = self.get_response(page=page, aid=aid)

                # 边爬取边保存
                df = pd.DataFrame(
                    {'评论时间': times, '评论者': uname, '评论内容': [''.join(comment.split()) for comment in comments],
                     '点赞数': likes})
                df.to_csv(f'{save_folder}/{title}.csv', encoding='utf-8-sig', index=False)

                print(f'\n\n已经保存 {df.shape[0]} 条评论到 {save_folder}/{title}.csv\n\n')

                sleep(1)

            # 每抓完 1 条视频的评论休眠 10s
            sleep(10)

    def get_Comment_to_DataBase(self, bvs):

        db = pymysql.connect(host="localhost",
                             user="root",
                             password="vs8824523",
                             database="bilibilicommentdb")

        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        if ("bilibilicommentdb",) not in tables:
            sql = """CREATE TABLE IF NOT EXISTS BiliBilicomment (
                          TITLE CHAR(50) NOT NULL,
                          TIME  TIMESTAMP,
                          UNAME CHAR(24),
                          LIKECOUNT BIGINT,
                          COMMENTS TEXT)"""
            cursor.execute(sql)

        if not isinstance(bvs, list):
            ValueError("传入的类型不是list")
        if not bvs:
            ValueError("未传入正确的Bv列表")
        for bv in bvs:
            print(bv)
            aid = self.get_aid(bv)
            title = self.get_title(bv)
            title = self.validateTitle(title=title)
            print(title)
            response = self.get_response(aid=aid)

            total_page = json.loads(response.text)['data']['page']['count'] // 20 + 1
            page = 1
            is_root, uname, comments, times, likes = [], [], [], [], []
            while True:
                print(response.text)
                data = json.loads(response.text)['data']['replies']
                if not data:
                    data = json.loads(response.text)['data']
                    if 'hots' in data.keys():
                        data = data['hots']
                    else:
                        break
                for row in data:
                    print('根评论', row['member']['uname'], row['content']['message'])
                    is_root.append('是')
                    times.append(self.intToStrTime(row['ctime']))
                    uname.append(row['member']['uname'])
                    comments.append(row['content']['message'])
                    likes.append(row['like'])
                    self.__insert_toDB(title=title, row=row, type="root")
                    if row.get('replies'):
                        for crow in row['replies']:
                            is_root.append('否')
                            times.append(self.intToStrTime(crow['ctime']))
                            uname.append(crow['member']['uname'])
                            comments.append(crow['content']['message'])
                            likes.append(crow['like'])
                            print(crow)
                            self.__insert_toDB(title=title,row=row,crow=crow)
                            print('---子评论', crow['member']['uname'], crow['content']['message'])

                page += 1
                if page > total_page:
                    break
                sleep(1)
                response = self.get_response(page=page, aid=aid)

                # print(f'\n\n已经保存 {df.shape[0]} 条评论到')

                sleep(1)

            # 每抓完 1 条视频的评论休眠 10s
            sleep(10)

    def __insert_toDB(self,title,row,type=None,**crow):
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="vs8824523",
                             database="bilibilicommentdb")

        cursor = db.cursor()
        if type == "root":
            insert = "INSERT INTO bilibilicomment(TITLE,\
                                TIME, UNAME,LIKECOUNT,COMMENTS)\
                                VALUES ('%s', '%s', '%s', '%s','%s')" % (
                title,
                self.intToStrTime(row['ctime']),
                row['member']['uname'],
                row['like'],
                row['content']['message'])
            try:
                db.begin()
                cursor.execute(insert)
                db.commit()
            except Exception as e:
                db.rollback()
                print(e)
        else:

            insert = "INSERT INTO bilibilicomment(TITLE,\
                                        TIME, UNAME,LIKECOUNT,COMMENTS)\
                                        VALUES ('%s', '%s', '%s', '%s','%s')" % (

                title,
                self.intToStrTime(crow["crow"]['ctime']),
                crow["crow"]['member']['uname'],
                crow["crow"]['like'],
                crow["crow"]['content']['message'])
            try:
                db.begin()
                cursor.execute(insert)
                db.commit()
            except Exception as e:
                db.rollback()
                print(e)


    def get_bangumidata(self):
        url = "https://api.bilibili.com/pgc/web/rank/list?day=3&season_type=1"
        print(requests.get(url, cookies=self.cookies, headers=DEFAULT_HEADERS).text)
        response = requests.get(url, cookies=self.cookies, headers=DEFAULT_HEADERS).text
        datas = json.loads(response)["result"]["list"]
        bofangliang = []
        rating = []
        title = []
        danmaku = []
        for data in datas:
            bofangliang.append(data["icon_font"]["text"])
            rating.append(data["rating"])
            title.append(data["title"])
            danmaku.append(data["stat"]["danmaku"])

        else:
            # print(title,rating,bofangliang,danmaku)
            df = pd.DataFrame(
                {'番名': title, '评分': rating, '播放量': bofangliang, '弹幕数': danmaku})
            df.to_csv(f'BilibiliTOP50.csv', encoding='utf-8-sig', index=False)

    def get_upvideo_bv(self, bvid="BV1im411R7UB"):
        # TODO: 未完工

        url = "https://api.bilibili.com/x/space/arc/search"

        parms = {
            "mid": 245645656,
            "pn": 1,
        }
        print(requests.get(url, headers=DEFAULT_HEADERS, cookies=self.cookies, params=parms).text)

    def history_title_get(self, data_count=1200):
        """
           爬取历史记录并保存为csv文件
           :data_count 爬取多少数据 最大为2000
           :return: None
           """
        save_folder = '个人信息'
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        oid = "0"
        view_at = "0"
        tilte_data = []
        for i in range(data_count // 20):
            print(f"上面的{oid}")
            url = f"https://api.bilibili.com/x/web-interface/history/cursor?max={oid}&view_at={view_at}&business=archive"
            json_data = json.loads(requests.get(url=url, headers=DEFAULT_HEADERS, cookies=self.cookies).text)
            all_jsondata = json_data["data"]["list"]
            for a in all_jsondata:
                print([a["title"], a["tag_name"], a["kid"], a["view_at"]])
                tilte_data.append([a["title"], a["tag_name"], a["kid"], a["history"]["bvid"]])
                oid = a["kid"]
                view_at = a["view_at"]
            print(oid)
            time.sleep(1.5)
        df = pd.DataFrame(tilte_data, columns=["tilte", "tag_name", "kid", "bvid"])
        df.to_csv(f"./个人信息{self.name}的历史记录.csv")

    def favlist_title_get(self):
        save_folder = '个人信息'
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        tilte_data = []
        for i in range(11):
            url = f"https://api.bilibili.com/x/v3/fav/resource/list?media_id=87591453&pn={i}&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web"
            jsondata = json.loads(requests.get(url=url, headers=DEFAULT_HEADERS, cookies=self.cookies).text)
            alldata = jsondata["data"]["medias"]
            for i in alldata:
                tilte_data.append([i["title"], i["intro"]])
                print(i["title"], i["intro"])
        df = pd.DataFrame(tilte_data, columns=["tilte", "intro"])
        df.to_csv(f"./个人信息/{self.name}的收藏夹.csv")

    def Cookies_name_get(self):
        # DedeUserID = self.cookies["DedeUserID"]
        # url = f"https://space.bilibili.com/{DedeUserID}"
        # print(requests.get("https://api.bilibili.com/x/space/v2/myinfo?",cookies=self.cookies,headers=DEFAULT_HEADERS).text)
        response = json.loads(requests.get("https://api.bilibili.com/x/space/v2/myinfo?", cookies=self.cookies,
                                           headers=DEFAULT_HEADERS).text)
        name = response["data"]["profile"]["name"]
        return name


class SpiderDB(Spider):
    def __init__(self,
                 database="Mysql",
                 user=None,
                 password=None,
                 host="localhost"):
        self.database = database

        super()


if __name__ == '__main__':
    Cookies = {
        "buvid4": "8DE86F88-30FC-D1A4-27D2-BF88267E398966862-022121620-Am315Z0S4rpEKgx9os3ZMA%3D%3D",
        "i-wanna-go-back": "-1",
        "buvid_fp_plain": "undefined",
        "is-2022-channel": "1",
        "header_theme_version": "CLOSE",
        "CURRENT_BLACKGAP": "0",
        "hit-new-style-dyn": "1",
        "CURRENT_PID": "00185d10-cd5e-11ed-9df4-331b246c567d",
        "enable_web_push": "DISABLE",
        "CURRENT_FNVAL": "4048",
        "buvid3": "2225C778-39E7-BA92-0CC3-08EBAD4D2C5949879infoc",
        "b_nut": "1702738750",
        "_uuid": "64223BE7-3175-85510-BAB7-D84992612FAA20993infoc",
        "hit-dyn-v2": "1",
        "_ga": "GA1.1.1459877433.1704103180",
        "_ga_HE7QWR90TV": "GS1.1.1704103179.1.1.1704104707.0.0.0",
        "rpdid": "|(k|kYmRklJY0J'u~|lm|lu|l",
        "FEED_LIVE_VERSION": "V8",
        "CURRENT_QUALITY": "116",
        "home_feed_column": "5",
        "fingerprint": "6a659a99af62e24c509eb9b46a1f4192",
        "buvid_fp": "2e8642a611476715b4f4f48c3ecee59e",
        "bsource": "search_bing",
        "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTA4Mjk0NjksImlhdCI6MTcxMDU3MDIwOSwicGx0IjotMX0.uglFonp9oJucna1h9NfyJ9_Tg_HDvqQ5e6JZ9dr5dkw",
        "bili_ticket_expires": "1710829409",
        "SESSDATA": "a67e3555%2C1726124211%2C4cc68%2A31CjAK3u3Xj4EJOT34UyC7tRV_g6wIyRyzay_3aCjx1ajS_XTQqiGPtSkyPdHtJuE25qsSVno4OEpYNzRmQUhkeVNJaldPTTZXMEVJajMtLXh4czk1UnRxWEh6eG0wYjZCQWN6eVM0bDNEYy1vQlFUYkJtWnlZREhIcGlyeWZEZzdzX2t0U192OXJ3IIEC",
        "bili_jct": "c5db9d38b933dadc4f45ecec48bf5730",
        "DedeUserID": "32347153",
        "DedeUserID__ckMd5": "6e20d89c04c0aaaa",
        "sid": "86a6m9ac",
        "bp_video_offset_32347153": "909390566814384166",
        "b_lsid": "64B48255_18E4641B361",
        "browser_resolution": "1706-924",
        "PVID": "3"
    }
    bvs = ["BV1Hw41177mh"]

    pachong = Spider(Cookies=Cookies)

    # pachong.get_Comment_to_DataBase(bvs)
    # pachong.get_Comment_tocsv(bvs)
    pachong.get_bangumidata()
    # pachong.history_title_get()
