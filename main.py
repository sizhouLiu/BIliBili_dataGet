"""
-*- coding : utf-8 -*-
主执行文件
@Author : Stupid_Cat
@Time : 2024/3/18 21:01
"""

import PyBiliBili as Pbl

bvs = ["BV1Xb4y1x7sP"]
c = {
    "nostalgia_conf": "-1",
    "CURRENT_PID": "bbd5a7e0-e0d9-11ed-b142-6d6c87db5b27",
    "buvid3": "3542C551-5636-BFCE-F526-827F29C0C31968482infoc",
    "i-wanna-go-back": "-1",
    "_uuid": "61F42B210-56C2-BE3D-6F4C-5F8C5581D98E68666infoc",
    "FEED_LIVE_VERSION": "V8",
    "b_nut": "1690363269",
    "header_theme_version": "CLOSE",
    "buvid4": "EA57EBB8-B730-E812-168D-3E00A9D687BA69565-023072617-8%2BoSQyln5YlQaVJTck8TEg%3D%3D",
    "rpdid": "|(uYml||kRJR0J'uYm|R~Ruku",
    "buvid_fp_plain": "undefined",
    "hit-new-style-dyn": "1",
    "hit-dyn-v2": "1",
    "b_ut": "5",
    "CURRENT_BLACKGAP": "0",
    "enable_web_push": "DISABLE",
    "LIVE_BUVID": "AUTO8616983179605434",
    "is-2022-channel": "1",
    "DedeUserID": "436457648",
    "DedeUserID__ckMd5": "e0058d6cf75e3e18",
    "sid": "6sqrciro",
    "bp_video_offset_436457648": "901621142796632115",
    "SESSDATA": "80a0e5ac%2C1724317215%2Cf6832%2A22CjDarWTjdYion2-TCpa1qMUdGaJ_QG6k6duPztCOrEarcnZZQIa0XMD0CMUjzvluhpsSVjhwVUNFVXlJd0xHeHpidk5sV1gxYndybW40U1FNbFNoU3BBLXVnUm1raGs2LWpJREtkcmxOelRIUGJoUXpaZ015UlY3ejVleFpyaHh2eHdLdGZaXzF3IIEC",
    "bili_jct": "0bf41c2c7cb44b0fe7dd7ed237519d4c",
    "fingerprint": "650da1a4f412b93dd8bff03c4ff76643",
    "CURRENT_FNVAL": "4048",
    "PVID": "2",
    "home_feed_column": "5",
    "buvid_fp": "2de3b34f1c83f12980e276ff67d91bc6",
    "bp_video_offset_2024972081": "911912610270543922",
    "browser_resolution": "1975-1011",
    "CURRENT_QUALITY": "80",
    "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTE0MjU3ODMsImlhdCI6MTcxMTE2NjUyMywicGx0IjotMX0.Xm_VfPqQc8KcNi5RBcWed_dvIZbcuZNzwshB7TxXsqo"
}

user = "root"
password = "vs8824523"
host = "localhost"
database = "bilibilicommentdb"

toDB = Pbl.SpidertoDB(user=user,
                  password=password,
                  host=host,
                  database=database)

# print("十连抽~~~~")
# for i in range(10):
#     """
#     十连抽~
#     """
#     Pbl.Spider.randbilibilivideourl()

enumerate

pachong = Pbl.Spider()

# video = Pbl.VideoSpider(Cookies=c)
# video.get_video("BV1V5411G7Qb")
# pachong.get_Comment_tocsv(bvs)
# pachong.get_Comment_tocsv([i[0] for i in pachong.get_Search_videos(keyword="那些无名之辈")])

# print(pachong.get_jsondata(bvs[0]))
# pachong.get_Comment_tocsv(bvs)
# pachong.history_title_get()
# pachong.history_data_get_toDB(data_count=1200,toDB=toDB)
# pachong.history_title_get()
# pachong.history_title_get()
# pachong.favlist_title_get()
pachong.hot_video_get()
# pachong.favlist_title_get()
# pachong.get_bangumidata()


