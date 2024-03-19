"""
-*- coding : utf-8 -*-
字符串常量声明与构造类
@Author : Stupid_Cat
@Time : 2024/3/16 14:54
"""


DEFAULT_HEADERS  ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
}

SALT = "ea1db124af3c7062474693fa704f4ff8"
# md5加的盐 话说盐应该怎么翻译

UP_VIDIO_DATA = {
        'mid': '3493110839511225',
        'ps': '30',
        'tid': '0',
        'pn': 1,
        'keyword': '',
        'order': 'pubdate',
        'platform': 'web',
        'web_location': '1550101',
        'order_avoided': 'true',
        'dm_img_list': '[]',
        'dm_img_str': 'V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ',
        'dm_cover_img_str': 'QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNjMwICgweDAwMDAzRTkyKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC',
        'w_rid': "w_rid",
        'wts': 1,
    }


COOKITES = {
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
    "DedeUserID": "32347153",
    "DedeUserID__ckMd5": "6e20d89c04c0aaaa",
    "LIVE_BUVID": "AUTO5017107285696779",
    "bsource": "search_bing",
    "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTEwODcxMTAsImlhdCI6MTcxMDgyNzg1MCwicGx0IjotMX0.qeUkW0vfYq4sExzg_LmOW8GVpIV5CCZzJ-LUEhmOAIM",
    "bili_ticket_expires": "1711087050",
    "b_lsid": "7E6EA7103_18E568D5932",
    "PVID": "1",
    "browser_resolution": "1707-426",
    "SESSDATA": "a1363d04%2C1726401265%2C8a015%2A32CjB6f4qAbVTIQi-gypB1lRAv-H260jGxcqFM6zOPozg6gqQ_OluDei4VZjbBBvgANdkSVkJOMDFabjBGQTVvOXBwUnlNZ2VqSEJ3eHpJQ2tVOXZuVjh1T1ZCQ0JiNVVEcjV4ZEJfR2ZsZzhRNUQ1Z0Q1WmJCMG5wYlZuaXppSVlvaGF1U29ibk5RIIEC",
    "bili_jct": "86061f88d3c10251b73b7c934e07c396",
    "fingerprint": "2e8642a611476715b4f4f48c3ecee59e",
    "bp_video_offset_32347153": "910583476810416195",
    "sid": "ml58ypqq",
    "buvid_fp": "2e8642a611476715b4f4f48c3ecee59e"
}

USER_HOME_PAGEW_PARAM = {  # 顺序很重要
    "dm_cover_img_str": "",
    "dm_img_list": "",
    'keyword': "",
    "mid": "userId",
    "order": "pubdate",
    "order_avoided": "true",
    "platform": "web",
    "pn": "pcursor",
    "ps": "30",
    "tid": "0",
    "web_location": "1550101",
    "wts": "str(int(time.time()))",
}
