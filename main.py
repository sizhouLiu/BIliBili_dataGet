from Bilibili爬取一览 import Spider

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
bvs = ["BV1M2421T7qk"]

pachong = Spider(Cookies=Cookies)

# pachong.get_Comment_to_DataBase(bvs)
# pachong.get_Comment_tocsv(bvs)
# pachong.get_bangumidata()
# pachong.history_title_get()
pachong.get_upvideo_bv()
