"""
-*- coding : utf-8 -*-
主执行文件
@Author : Stupid_Cat
@Time : 2024/3/18 21:01
"""

import PyBiliBili as Pbl
from tqdm import tqdm

bvs = ["BV1Xb4y1x7sP"]
user = "Your Database username"
password = "password"
host = "host"
database = "databasename"

# toDB = Pbl.SpidertoDB(user=user,
#                   password=password,
#                   host=host,
#                   database=database)

# print("十连抽~~~~")
# for i in range(10):
#     """
#     十连抽~
#     """
#     Pbl.Spider.randbilibilivideourl()

pachong = Pbl.Spider()

video = Pbl.VideoSpider()

# video = Pbl.VideoSpider()
# video.get_video("BV1F3411J793")
# pachong.get_Comment_tocsv(bvs)
# pachong.get_Comment_tocsv([i[0] for i in pachong.get_Search_videos(keyword="那些无名之辈")])

# print(pachong.get_jsondata(bvs[0]))
# pachong.get_Comment_tocsv(bvs)
# pachong.history_title_get()
# pachong.history_data_get_toDB(data_count=1200,toDB=toDB)
# pachong.history_title_get()
# pachong.history_title_get()
# pachong.favlist_title_get()
# pachong.hot_video_get()
# pachong.favlist_title_get()
# pachong.get_bangumidata()


# 一个按关键词下载视频的例子
serch_res = pachong.get_Search_videos()

for i in tqdm(serch_res, desc="Processing videos", unit="video"):
    cid, title = video.get_cid(i[0])
    if cid and title:
        print(f"视频名称: {title}")
        video.get_video(i[0])
    else:
        print(f"Skipping video with bvid: {i[0]} due to missing data.")
