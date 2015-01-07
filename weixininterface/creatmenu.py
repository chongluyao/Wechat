# -*- coding:utf-8 -*-
from wechat.settings import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib2
import urllib
import json

def createmenu(buttons):

    #print buttons
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+WEIXIN_APPID+'&secret='+WEIXIN_SECRET


    response = urllib2.urlopen(url)
    html = response.read()
    tokeninfo = json.loads(html)
    token = tokeninfo['access_token']
    #print token

    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + str(token)

    # print url

    req = urllib2.Request(url, buttons)
    # print req

    response = urllib2.urlopen(req)
    #print response

    return response

buttons = '''
{
    "button": [
        {
            "name": "我要弃疗",
            "sub_button": [
                {
                    "type": "click",
                    "name": "开脑洞",
                    "key": "COURSE_ND"
                },
                {
                    "type": "click",
                    "name": "猜歌名",
                    "key": "COURSE_MS"
                },
                {
                    "type": "click",
                    "name": "点歌台",
                    "key": "ORDERSONG"
                },
                {
                    "type": "click",
                    "name": "猜数字",
                    "key": "GUESSNUMBER"
                }
            ]
        },
        {
            "name": "我要学习",
            "sub_button": [
                {
                    "type": "click",
                    "name": "软基",
                    "key": "COURSE_ST"
                },
                {
                    "type": "click",
                    "name": "操统",
                    "key": "COURSE_OS"
                },
                {
                    "type": "click",
                    "name": "软工",
                    "key": "COURSE_SE"
                },
                {
                    "type": "click",
                    "name": "计网",
                    "key": "COURSE_CN"
                }
            ]
        },
        {
            "name": "排行榜",
            "type": "view",
            "url": "http://4.thsswelearn.sinaapp.com/ranking"
        }
    ]
}'''

createmenu(buttons)