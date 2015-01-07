# -*- coding: UTF-8 -*-
from weixininterface.question_handler import *
import random
import urllib2

numLen = 5

def event_gamehandler(user):
    #quit_msg = quit_reply(user)
    reply_msg = u"欢迎来到%d位猜数字游戏！\n" % numLen
    reply_msg += u"输入“规则”可以查看游戏规则,或直接开始猜测！"
    answer = ""
    order = ['0','1','2','3','4','5','6','7','8','9']
    random.shuffle(order)
    for i in range(numLen):
        answer += order[i]
    user.state = "GUESSNUMBER_0_" + answer
    user.save()
    return reply_msg

def text_gamehandler(user, msg):
    state = user.state
    if u'规则' in msg or 'rule' in msg:
        reply_msg = u"我们将随机生成%s位不含重复数字的数,\n" % numLen
        reply_msg += u"您每猜一个数字，就要根据这个数字给出几A几B,\n"
        reply_msg += u"其中A前面的数字表示位置正确的数的个数,\n"
        reply_msg += u"而B前的数字表示数字正确而位置不对的数的个数。\n"
        return reply_msg
    if len(msg) != numLen:
        reply_msg = u"输入有误，请输入%s位数字\n" % numLen
        return reply_msg
    for i in range(numLen):
        if not msg[i] in ['0','1','2','3','4','5','6','7','8','9']:
            reply_msg = u"输入有误，请输入%s位数字\n" % numLen
            return reply_msg
    step = int(state.split('_')[1])
    answer = state.split('_')[2]
    user.state = 'GUESSNUMBER_' + str(step+1) + '_' + answer
    user.save()
    a = b = 0
    for i in range(numLen):
        if msg[i] == answer[i]:
            a = a + 1
        elif msg[i] in answer:
            b = b + 1
    reply_msg = u"【%dA%dB】" % (a,b)
    if a == numLen:
        user.state = "NONE"
        user.save()
        reply_msg += u"恭喜你成功猜出了数字%s,共计猜了%d次。\n" % (answer, step)
        reply_msg += u"击败了全国%d%%的玩家\n" % random.randrange(0,100)
    return reply_msg

def event_ordersonghandler(user):
    reply_msg = u"欢迎来到点歌台!\n"
    reply_msg += u"输入“规则”可以查看点歌规则~"
    user.state = 'ORDERSONG'
    user.save()
    return reply_msg

def text_ordersonghandler(user, content):

    if content == "规则" or content == "rule":
        reply_msg = u"输入格式为【歌曲名称】或【歌曲名称#歌手】\n"
        reply_msg += u"使用后者格式更容易搜出符合你需求的歌曲哟~"
        return reply_msg

    musicTitle = u""
    musicAuthor = u""
    if len(content.split("#")) == 1:
        musicTitle = content.split("#")[0]
        print musicTitle
        return getMusicUrl(musicTitle, musicAuthor)
    elif len(content.split("#")) == 2:
        musicTitle = content.split("#")[0]
        musicAuthor = content.split("#")[1]
        return getMusicUrl(musicTitle, musicAuthor)
    else:
        reply_msg = u"歌曲格式有误！\n"
        reply_msg += u"输入“规则”可以查看点歌规则~"
        return reply_msg

def getMusicUrl(musicTitle, musicAuthor):
    #url = "http://cdn.y.baidu.com/yinyueren/58c935563924b95a2ea00a137a2da663.mp3?xcode=f250235c9759e62b8e2b54fb4ad6bebfe158b0c71b9245bb"
    #return ["abc", "ccc",url]

    searchUrl = "http://box.zhangmen.baidu.com/x?op=12&count=1&title="
    if searchUrl:
        searchUrl = searchUrl + musicTitle.replace(" ","%20") + '$$'
    else:
        return "0"
    if musicAuthor:
        searchUrl = searchUrl + musicAuthor.replace(" ","%20") + '$$$$'

    print searchUrl

    req = urllib2.Request(searchUrl)
    res_data = urllib2.urlopen(req)
    xml_str = res_data.read()

    print xml_str

    #xml = ET.fromstring(xml_str)
    count = xml_str[(xml_str.find('<count>')+7):xml_str.find('</count>')]
    print count
    type = xml_str[(xml_str.find('<type>')+6):xml_str.find('</type>')]
    print type
    if count < '1' or type != '8':
        print "search failed!"
        return u"根据相关法律法规和政策，搜索结果未予显示。"
    #former = "http://zhangmenshiting.baidu.com/data2/music/87364008/aWlmamlmZ3Bfn6NndK6ap5WXcJWYbpiaY2uVaGuYaZyVa5mYa5tnaGRll2pubGhtk2tkZJhmmp5ql5VsaWxwaGFoalqin5t1YWBqaGtqaXBmZmdsZmpnaTE$"
    former = xml_str.split('![CDATA[')[1]
    print former
    former = former[:former.find(']]>')]
    print former
    former = former.replace(former.split('/')[len(former.split('/'))-1],"")
    print former
    #latter = "87364008.mp3?xcode=ac8ab29b46b2dd9fd6e0033d69615b910c0cf9eb84690067&mid=0.74642854481401"
    latter = xml_str.split('![CDATA[')[2]
    print latter
    latter = latter[:latter.find(']]>')]
    print latter
    if '&mid' in latter:
        latter = latter[:latter.find('&mid')]
    print latter

    # url = former.replace(former.split('/')[6], latter[:latter.find('&mid')])
    url = former + latter
    print url

    if not musicAuthor:
        musicAuthor = "未知的歌手"
    return [musicTitle, musicAuthor, url]
