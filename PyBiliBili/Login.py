"""
-*- coding : utf-8 -*-
登录类
@Author : Stupid_Cat
@Time : 2024/4/9 21:01
"""
import json
import logging
import os
import time

import qrcode
import requests

from PyBiliBili.DefaulString import DEFAULT_HEADERS


class Login(object):

    def __init__(self, Cookies=None):
        self.session = requests.session()
        self.cookies = Cookies
        if Cookies is None:
            self.cookies = self.__Login()
        self.name = self.__Cookies_name_get()

    def get_cookies(self):
        self.session.get("https://www.bilibili.com/", headers=DEFAULT_HEADERS)
        print(self.session.cookies)
        return self.session.cookies

    def __islogin(self):
        """
        通过接口判断Cookies 是否失效
        """

        loginurl = self.session.get("https://api.bilibili.com/x/web-interface/nav", verify=False,
                                    headers=DEFAULT_HEADERS).json()
        if loginurl['code'] == 0:
            logging.info('Cookies值有效，{}，已登录！'.format(loginurl['data']['uname']))

            return True
        else:
            logging.error('Cookies值已经失效，请重新扫码登录！')
            return False

    def __Login(self):
        """
        扫码登录BIliBili获取Cookies
        登录后会存放到Cookies.json文件
        如果Cookies失效
        则重新扫码登录
        return Cookies
        """
        if not os.path.exists('Cookies.json'):
            with open("Cookies.json", 'w') as f:
                f.write("{}")
        with open("Cookies.json", "r") as f:
            self.session.cookies = requests.utils.cookiejar_from_dict(json.load(f))

        status = self.__islogin()
        # 获取登录状态 若Cookies失效则生成二维码登录
        if not status:
            url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
            response = json.loads(requests.get(url=url, headers=DEFAULT_HEADERS, cookies=self.cookies).text)
            qrcode_key = response["data"]["qrcode_key"]
            login_url = response["data"]["url"]
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_Q,
                box_size=10,
                border=4,
            )
            # 将链接添加到QRCode对象中
            qr.add_data(login_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("link_qrcode.png")
            img.show()
            params = {
                "qrcode_key": qrcode_key
            }
            weblogin_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"

            # logging.info(self.session.get(url=weblogin_url, params=params, cookies=self.cookies,
            #                        headers=DEFAULT_HEADERS).text)
            self.wait_qrcode(weblogin_url=weblogin_url,params=params)
            self.cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            with open("Cookies.json", "w") as f:
                f.write(json.dumps(self.cookies))
            logging.info(self.session.cookies.items())

        return self.session.cookies

    def __Cookies_name_get(self):
        response = json.loads(requests.get("https://api.bilibili.com/x/space/v2/myinfo?", cookies=self.cookies,
                                           headers=DEFAULT_HEADERS).text)
        name = response["data"]["profile"]["name"]
        return name

    def wait_qrcode(self, weblogin_url, params):
        time.sleep(15)
        count = 10
        print(json.loads(self.session.get(url=weblogin_url,
                                           params=params,
                                           cookies=self.cookies,
                                           headers=DEFAULT_HEADERS
                                           ).text))
        while count > 0:
            if json.loads(self.session.get(url=weblogin_url,
                                           params=params,
                                           cookies=self.cookies,
                                           headers=DEFAULT_HEADERS
                                           ).text).get("data", {}).get("message","0") in ["未扫码", "二维码已扫码未确认"]:

                logging.info(self.session.get(url=weblogin_url,
                                       params=params,
                                       cookies=self.cookies,
                                       headers=DEFAULT_HEADERS
                                       ).text)
                time.sleep(10)
                count -= 1
            else:
                break
        return json.loads(self.session.get(url=weblogin_url,
                                               params=params,
                                               cookies=self.cookies,
                                               headers=DEFAULT_HEADERS
                                               ).text).get("message", "1")
