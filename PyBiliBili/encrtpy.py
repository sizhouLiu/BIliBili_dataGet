"""
-*- coding : utf-8 -*-
加密功能类
@Author : Stupid_Cat
@Time : 2024/3/18 21:01
"""


import base64
import hashlib
import random


def calculate_md5(string):
    # 通过hashlib模块创建了一个MD5哈希算法的实例
    md5_hash = hashlib.md5()
    # 使用UTF-8编码将输入字符串转换为字节，并将其更新到哈希对象中
    md5_hash.update(string.encode('utf-8'))
    # 计算得到的MD5哈希值的十六进制表示
    return md5_hash.hexdigest()

def base64_encode(encoded_str, encode='utf-8'):
    """
    Base64解密函数
    :param encoded_str: Base64编码的字符串
    :return: 原始的二进制数据
    """
    encoded_str = encoded_str.encode(encode)
    encoded_str = base64.b64encode(encoded_str)
    encoded_str = encoded_str.decode()
    return encoded_str.strip('=')


def get_dm_cover_img_str(num=650):
    num = random.randrange(350, 651)
    sss = f'ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics {num}, OpenGL 4.1)Google Inc. (Intel Inc.)'
    dm_cover_img_str = base64_encode(sss)
    return dm_cover_img_str


def get_w_rid(date_time,page=1):
    # date_time = int(time.time())
    f = [
        "dm_cover_img_str=QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNjMwICgweDAwMDAzRTkyKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC",
        "dm_img_list=%5B%5D",
        "dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
        "keyword=",
        "mid=3493110839511225",
        "order=pubdate",
        "order_avoided=true",
        "platform=web",
        f"pn={page}",
        "ps=30",
        "tid=0",
        "web_location=1550101",
        f"wts={date_time}"
    ]
    y = '&'.join(f)
    w_rid = calculate_md5(y + "ea1db124af3c7062474693fa704f4ff8")
    return w_rid