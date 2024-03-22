"""
-*- coding : utf-8 -*-
主执行文件
@Author : Stupid_Cat
@Time : 2024/3/18 21:01
"""


from Bilibili_data_get import Spider,SpidertoDB
from DefaulString import COOKITES

bvs = ["BV11f421f7ze"]
pachong = Spider(Cookies=COOKITES)

user = "root"
password = "vs8824523"
host = "localhost"
database = "bilibilicommentdb"

# pachong.get_Comment_tocsv(bvs)
pachong.history_title_get()
# toDB = SpidertoDB(user=user,
#                   password=password,
#                   host=host,
#                   database=database)
# a = pachong.get_upvideo_bv(1140672573, page=2, max_page=6)
# for i in a:
#     print([i[1]])
#     pachong.get_Comment_to_DataBase([i[1]], toDB=toDB)
#

