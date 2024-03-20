"""
-*- coding : utf-8 -*-
数据获取功能类
@Author : Stupid_Cat
@Time : 2024/3/16 14:54
"""

import requests
import os
import json
import time
import pandas as pd
import re
import pymysql


import DefaulString
from string_format import validateTitle, intToStrTime
from time import sleep
from DefaulString import DEFAULT_HEADERS
from BIlibiliupBV import get_up_video_data


class Spider(object):

    def __init__(self, Cookies):
        self.cookies = Cookies
        self.name = self.Cookies_name_get()

    def __del__(self):
        print("爬取结束！")

    def get_cookies(self):
        cookies = requests.get("https://www.bilibili.com/", headers=DEFAULT_HEADERS).cookies
        return cookies

    def get_jsondata(self,bv):
        """
        bv：bv号
        return：评论的json格式
        """
        response = requests.get(url=f'https://www.bilibili.com/video/{bv}', headers=DEFAULT_HEADERS)
        res = re.findall('<script>window.__INITIAL_STATE__=(.*)?;\(function\(\)', response.text, re.S)

        json_data = json.loads(res[0])
        if 'message' in json_data['error']:
            print(json_data['error']['message'])
            return Exception("错误")
        return json_data

    def get_aid(self, json_data):
        aid = json_data['aid']
        return aid

    def get_title(self, json_data):

        title = json_data['videoData']['title']
        return title

    def get_upname(self,json_data):
        name = json_data["videoData"]["owner"]["name"]
        print(name)
        return name


    def get_desc(self,json_data):
        desc = json_data["videoData"]["desc"]
        print(desc)
        return desc


    def get_response(self, aid, page=1):
        video_info_url = 'https://api.bilibili.com/x/web-interface/archive/relation?aid={}'.format(aid)

        # res_json = requests.get(url=video_info_url, headers=DEFAULT_HEADERS, cookies=self.cookies).json()
        # print(res_json)
        # like_count, coin_count, collection_count = res_json['data']['like'], res_json['data']['coin'], res_json['data']['favorite']
        # print(aid, title, like_count, coin_count, collection_count)

        comment_url = 'https://api.bilibili.com/x/v2/reply?callback=jQueryjsonp=jsonp&pn={}&type=1&oid={}&sort=2&_=1594459235799'
        response = requests.get(url=comment_url.format(page, aid), headers=DEFAULT_HEADERS,
                                cookies=DefaulString.COOKITES)

        return response

    def get_Comment_tocsv(self, bvs):
        """
        bvs:BV号的列表
        return: 无返回值 会生成一个以视频名命名的.csv数据
        """
        save_folder = 'Comment'
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)

        if not isinstance(bvs, list):
            ValueError("传入的类型不是list")
        if not bvs:
            ValueError("未传入正确的Bv列表")
        for bv in bvs:
            print(bv)
            jsondata = self.get_jsondata(bv)
            aid = self.get_aid(jsondata)
            title = self.get_title(jsondata)
            title = validateTitle(title=title)
            response = self.get_response(aid=aid)


            total_page = json.loads(response.text)['data']['page']['count'] // 20 + 1
            page = 1
            is_root, uname, comments, times, likes, sex = [], [], [], [], [], []
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
                    print('根评论', row['member']['uname'], row['content']['message'],row['member']['sex'])
                    sex.append(row['member']['sex'])
                    is_root.append('是')
                    times.append(intToStrTime(row['ctime']))
                    uname.append(row['member']['uname'])
                    comments.append(row['content']['message'])
                    likes.append(row['like'])

                    if row.get('replies'):
                        for crow in row['replies']:
                            is_root.append('否')
                            sex.append(crow['member']['sex'])
                            times.append(intToStrTime(crow['ctime']))
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
                     '点赞数': likes,"性别":sex})
                df.to_csv(f'{save_folder}/{title}.csv', encoding='utf-8-sig', index=False)

                print(f'\n\n已经保存 {df.shape[0]} 条评论到 {save_folder}/{title}.csv\n\n')

                sleep(1)

            # 每抓完 1 条视频的评论休眠 10s
            sleep(10)

    def get_Comment_to_DataBase(self, bvs,toDB):
        """
        bvs:BV号的列表
        toDB：一个SpiderDB实例用于数据存储
        """

        toDB.create_table()
        if not isinstance(bvs, list):
            ValueError("传入的类型不是list")
        if not bvs:
            ValueError("未传入正确的Bv列表")
        count = 0
        for bv in bvs:
            print(bv)
            jsondata = self.get_jsondata(bv)
            aid = self.get_aid(jsondata)
            title = self.get_title(jsondata)
            title = validateTitle(title=title)
            print(title)
            response = self.get_response(aid=aid)
            upname = self.get_upname(jsondata)
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
                    times.append(intToStrTime(row['ctime']))
                    uname.append(row['member']['uname'])
                    comments.append(row['content']['message'])
                    likes.append(row['like'])
                    count += 1
                    toDB.insert_toDB(title=title, upname=upname, row=row, type="root")
                    if row.get('replies'):
                        for crow in row['replies']:
                            is_root.append('否')
                            times.append(intToStrTime(crow['ctime']))
                            uname.append(crow['member']['uname'])
                            comments.append(crow['content']['message'])
                            likes.append(crow['like'])

                            toDB.insert_toDB(title=title, upname=upname, row=crow)
                            print('---子评论', crow['member']['uname'], crow['content']['message'])
                            count += 1
                page += 1
                if page > total_page:
                    break
                sleep(1.5)
                response = self.get_response(page=page, aid=aid)

                print(f'\n\n已经保存 {count} 条评论到bilibilicommentdb')

            # 每抓完 1 条视频的评论休眠 10s
            sleep(10)

    @staticmethod
    def get_bangumidata():
        """
        获取bilibili番剧排行榜top50的csv数据
        """
        url = "https://api.bilibili.com/pgc/web/rank/list?day=3&season_type=1"
        print(requests.get(url, cookies=DefaulString.COOKITES, headers=DEFAULT_HEADERS).text)
        response = requests.get(url, cookies=DefaulString.COOKITES, headers=DEFAULT_HEADERS).text
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
            print(title, rating, bofangliang, danmaku)
            df = pd.DataFrame(
                {'番名': title, '评分': rating, '播放量': bofangliang, '弹幕数': danmaku})
            df.to_csv(f'BilibiliTOP50.csv', encoding='utf-8-sig', index=False)

    def get_Search_videos(self,keyword="原神",search_type="video",order="totalrank",page=1):
        """
        该函数用于获取B站搜索视频的bv号标题等数据
        page:页码
        keyword:关键字 查询的视频标题 默认为原神
        search_type：搜索目标类型:{视频：video
                                番剧：media_bangumi
                                影视：media_ft
                                直播间及主播：live
                                直播间：live_room
                                主播：live_user
                                专栏：article
                                话题：topic
                                用户：bili_user
                                相簿：photo}
        order:结果排序方式：{搜索类型为视频、专栏及相簿时：
                                默认为totalrank
                                综合排序：totalrank
                                最多点击：click
                                最新发布：pubdate
                                最多弹幕：dm
                                最多收藏：stow
                                最多评论：scores
                                最多喜欢：attention（仅用于专栏）
                                ----------------------------
                                搜索结果为直播间时：
                                默认为online
                                人气直播：online
                                最新开播：live_time
                                ----------------------------
                                搜索结果为用户时：
                                默认为0
                                默认排序：0
                                粉丝数：fans
                                用户等级：level}
        return:list->[BV号，标题，播放量，UP主ID，视频地址]
                        """
        url = "https://api.bilibili.com/x/web-interface/wbi/search/type"
        params = {"keyword": keyword,
                  "search_type": search_type,
                  "order": order,
                  "page": page}
        response = requests.get(url=url, params=params,cookies=self.cookies, headers=DEFAULT_HEADERS).json()
        json_datas = response["data"]["result"]
        return [[json_data["bvid"],json_data["title"],json_data["play"],json_data["author"],json_data["arcurl"]]for json_data in json_datas]

    def get_upvideo_bv(self, mid, page=1, max_page=3):
        """

        :param mid: up主的id号 视频空间连接上的数字
        :param page: 起始投稿页
        :param max_page: 最大页
        :return: 返回一个list->[视频标题,视频BV号,视频评论数,视频播放量]
        """
        # TODO: 可以使用 但是代码不够规范 需要调整

        return [[video["title"], video["bvid"], video["comment_num"], video["play_num"]] for video in
                get_up_video_data(mid, pcursor=page, max_list_page=max_page)]

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
        df = pd.DataFrame(tilte_data, columns=["title", "tag_name", "kid", "bvid"])
        df.to_csv(f"./个人信息/{self.name}的历史记录.csv")

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
                # print(i["title"], i["intro"])
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


class SpidertoDB():
    # TODO：我想着写一个专门做数据库存储的类 没想好怎么写阿（＞人＜；）
    def __init__(self,
                 database="",
                 user=None,
                 password=None,
                 host="localhost"):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.db = pymysql.connect(host=self.host,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database)

    def __del__(self):
        """
        在类被回收时关闭连接
        """
        print("数据库连接关闭")
        self.db.close()

    def __sql_toDB_judge(self, sql):
        try:
            self.db.begin()
            self.db.cursor().execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)

    def insert_toDB(self, title, upname, row, type=None):
        if type == "root":
            insert = "INSERT INTO bilibilicomment(TITLE,UPNAME,\
                                   TIME, UNAME,LIKECOUNT,COMMENTS)\
                                   VALUES ('%s', '%s', '%s', '%s', '%s','%s')" % (
                title,
                upname,
                intToStrTime(row['ctime']),
                row['member']['uname'],
                row['like'],
                row['content']['message'])
            self.__sql_toDB_judge(insert)
        else:

            insert = "INSERT INTO bilibilicomment(TITLE,UPNAME,\
                                              TIME, UNAME,LIKECOUNT,COMMENTS)\
                                              VALUES ('%s', '%s', '%s', '%s', '%s','%s')" % (

                title,
                upname,
                intToStrTime(row['ctime']),
                row['member']['uname'],
                row['like'],
                row['content']['message'])
            self.__sql_toDB_judge(insert)

    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        if ("bilibilicommentdb",) not in tables:
            sql = """CREATE TABLE IF NOT EXISTS BiliBilicomment (
                          TITLE CHAR(50) NOT NULL,
                          UPNAME CHAR(40) NOT NULL,
                          TIME  TIMESTAMP,
                          UNAME CHAR(24),
                          LIKECOUNT BIGINT,
                          COMMENTS TEXT)"""
            cursor.execute(sql)

    def delete_Redundant_data(self):
        # TODO: 去除重复数据 SQL语句条件判断错误把我的表给清空了 暂时搁置阿(´。＿。｀)

        pass
        # sql = """DELETE FROM BiliBilicomment WHERE ;"""
        #
        # sql = """
        # DELETE FROM BiliBilicomment
        # WHERE COMMENTS = COMMENTS
        # """

        # try:
        #     # 执行 SQL 语句
        #     self.db.cursor().execute(sql)
        #     self.db.commit()  # 提交操作到数据库
        #     print("重复数据删除成功")
        # except Exception as e:
        #     print("删除重复数据失败:", e)
        #     self.db.rollback()  # 回滚操作
        #
        # # 关闭数据库连接
        # self.db.close()

if __name__ == '__main__':

    bvs = ["BV11f421f7ze"]
    pachong = Spider(Cookies=DefaulString.COOKITES)

    user = "root"
    password = "vs8824523"
    host = "localhost"
    database = "bilibilicommentdb"
    toDB = SpidertoDB(user=user,
                      password=password,
                      host=host,
                      database=database)
    pachong.get_Comment_to_DataBase(bvs,toDB)
    # toDB.delete_Redundant_data()
    # a = pachong.get_upvideo_bv(1140672573, page=3, max_page=6)
    # for i in a:
    #     print([i[1]])
    #     pachong.get_Comment_to_DataBase([i[1]],toDB=toDB)
    #     sleep(10)
    # pachong.get_Search_videos()
