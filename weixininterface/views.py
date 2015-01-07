# -*- coding: UTF-8 -*-
from django.shortcuts import render

# Create your views here.
#from weixininterface.models import *
from django.views.generic.base import View
import hashlib
from django.http import HttpResponse, HttpResponseRedirect
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from wechat.settings import *
from weixininterface.question_handler import *
from weixininterface.game_handler import *
import weixininterface.creatmenu
import time
import random
from operator import attrgetter


class ranking_handler(View):
    def get(self, request, *args, **kwargs):
        courses = [course for course in Course.objects.all() if course.name in ["ND", "MS", "OS", "SE", "CN",  "ST"]]
        bestPlayers = []
        for course in courses:
            bestPlayer = CoursesRecord.objects.filter(course = course)
            bestPlayer = list(bestPlayer)
            bestPlayer.sort(key=attrgetter("score"), reverse = True)
            bestPlayers.append(([(self.filterNickname(onebestplayer.player.nickname, index),
                u"：" + str(onebestplayer.score * 100 / len(Question.objects.filter(course = course)))) for index, onebestplayer in enumerate(bestPlayer)] + [(u"等你来战！", "")] * 6)[:6])

        tempresult = []
        position = "100%"
        for title, tempplayerresult in zip(courses[1:], bestPlayers[1:]):
            tempresult.append({"title":'【%s】' % real_course_name(title.name), "result":[item for item in tempplayerresult], "position":position})
        result = {"result0":{"title":'【%s】' % real_course_name(courses[0].name), "result":bestPlayers[0], "position":position}, "result":tempresult}
        return render(request, 'ranking.html', result)
    def filterNickname(self, nickname, index):
        award = [u"第零名", u"第一名", u"第二名", u"第三名", u"第四名", u"第五名"]
        if len(nickname) > 8:
            return award[index] + u"：" + nickname[:6] + ".."
        else:
            return award[index] + u"：" + nickname


class weixininterface(View):
    def _init_(self):
        self.TOKEN = 'weixin_token'
    def get(self, request, *args, **kwargs):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        alist = [WEIXIN_TOKEN, timestamp, nonce]
        alist.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, alist)
        if signature == sha1.hexdigest():
            return HttpResponse(echostr)

    def post(self, request, *args, **kwargs):
        xml_str = request.body
        xml = ET.fromstring(xml_str)
        (reply_msg, reply_msgType) = msg_handler(xml)
        #reply_msg = 'test'
        #reply_msgType = 'text'
        reply = reply_handler(xml, reply_msg, reply_msgType)
        return HttpResponse(mark_safe(reply), content_type="application/xml")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(weixininterface, self).dispatch(*args, **kwargs)


def msg_handler(xml):
    fromUserName = xml.find('FromUserName').text
    if not (Player.objects.filter(uid=fromUserName)):
        u1 = Player(uid=fromUserName, state='NONE')
        u1.save()
    user = Player.objects.get(uid=fromUserName)
    msgType = xml.find('MsgType').text
    if (msgType == 'event'):
        event = xml.find('Event').text
        if event == 'subscribe':
            reply_msg = u'欢迎来到【学习VS弃疗】\n'
            reply_msg += u'请留下您不太大的大名'
            reply_msgType = 'text'
            return (reply_msg, reply_msgType)
        if event == 'unsubscribe':
            user.nickname = ''
            user.save()
            reply_msg = '取消订阅'
            reply_msgType = 'text'
            return (reply_msg, reply_msgType)
        if user.nickname == '':
            reply_msg = u'请留下您不太大的大名'
            reply_msgType = 'text'
            return (reply_msg, reply_msgType)

        eventKey = xml.find('EventKey').text
        if eventKey.startswith('GUESSNUMBER'):
            reply_msg = event_gamehandler(user)
        elif eventKey.startswith('ORDERSONG'):
            reply_msg = event_ordersonghandler(user)
        else:
            reply_msg = event_questionhandler(user, eventKey)
    elif (msgType == 'text'):
        content = xml.find('Content').text

        if user.nickname == "":
            if len(content) > 9:
                reply_msg = u"您的大名如雷贯耳，但是太大了！"
            else:
                user.nickname = content
                user.save()
                reply_msg = u"昵称“%s”设置成功！\n" % user.nickname
                reply_msg += u"现在可以点击菜单来玩耍啦~"
                #reply_msg += u"\n擅自切换代码不会保存原来的状态哟！"
            reply_msgType = 'text'
            return (reply_msg, reply_msgType)

        if user.state.startswith('GUESSNUMBER'):
            reply_msg = text_gamehandler(user, content)
        elif user.state.startswith('ORDERSONG'):
            reply_msg = text_ordersonghandler(user, content)
        elif user.state.startswith('COURSE'):
            reply_msg = text_questionhandler(user, content)
        else:
            re = random.randrange(0,6)
            if re == 0:
                reply_msg = u'咦？我不知道你要干嘛哟~'
            elif re == 1:
                reply_msg = u'不要调戏人家嘛~'
            elif re == 2:
                reply_msg = u'莫名其妙..'
            elif re == 3:
                reply_msg = u'你是理工男吧……'
            elif re == 4:
                reply_msg = u'呵呵'
            else:
                reply_msg = u'interesting'

    if user.state.startswith('COURSE_MS'):
        reply_msgType = 'music'
    elif user.state.startswith('ORDERSONG'):
        if "http" in reply_msg[2]:
            reply_msgType = 'music'
        else:
            reply_msgType = 'text'
    else:
        reply_msgType = 'text'
    return (reply_msg, reply_msgType)


def reply_handler(xml, reply_msg, reply_msgType):
    fromUserName = xml.find('FromUserName').text
    toUserName = xml.find('ToUserName').text
    createTime = xml.find('CreateTime').text
    if (reply_msgType == 'text'):
        reply = '''
            <xml>
            <ToUserName>%s</ToUserName>
            <FromUserName>%s</FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType>%s</MsgType>
            <Content>%s</Content>
            </xml>''' % (fromUserName, toUserName, str(int(time.time())), reply_msgType, reply_msg)
    elif (reply_msgType == 'music'):
        reply = '''
            <xml>
            <ToUserName>%s</ToUserName>
            <FromUserName>%s</FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType>%s</MsgType>
            <Music>
                <Title>%s</Title>
                <Description>%s</Description>
                <MusicUrl>%s</MusicUrl>
                <HQMusicUrl>%s</HQMusicUrl>
            </Music>
            </xml>''' % (fromUserName, toUserName, str(int(time.time())), 'music',
                         reply_msg[0], reply_msg[1], reply_msg[2], reply_msg[2])
    return reply