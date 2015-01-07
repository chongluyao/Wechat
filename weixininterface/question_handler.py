# -*- coding: UTF-8 -*-
from django.utils.safestring import mark_safe
import random
from weixininterface.models import *

def real_course_name(course_name):
    if course_name == 'MS':
        return u'猜歌名'
    elif course_name == 'ND':
        return u'开脑洞'
    elif course_name == 'ST':
        return u'软基'
    elif course_name == 'OS':
        return u'操统'
    elif course_name == 'SE':
        return u'软工'
    elif course_name == 'CN':
        return u'计网'
    else:
        return course_name

def event_questionhandler(user, eventKey):
    course_name = eventKey.split('_')[1]
    #quit_msg = quit_reply(user)
    question_msg = begin_answer_question(user, course_name)
    if course_name == 'MS':
        reply = question_msg
        return reply
    else:
        reply = question_msg
        return reply


# def quit_reply(user):
#     reply = ''
#     state = user.state
#     if state.startswith('GUESSNUMBER'):
#         reply += u'''已经结束本轮猜数字！\n'''
#         reply += u'--------------------------\n'
#     elif state.startswith('COURSE'):
#         state_list = state.split('_')
#         question_number = len(state_list[2].split(',')) - 1
#         course_name = state_list[1]
#         if course_name == 'MS':
#             reply += u'''猜歌名结束,共猜对%d首歌！''' % question_number
#         else:
#             reply += u'''【%s】答题结束,共答对%d道题！''' % (real_course_name(course_name), question_number)
#         ranking = update_record(user, state_list)
#         if ranking:
#             reply += u'''\n恭喜进入【%s】排行榜！\n''' % real_course_name(course_name)
#         reply += u'\n--------------------------\n'
#     return reply


def begin_answer_question(user, course_name):
    try:
        current_course = Course.objects.get(name = course_name)
    except:
        user.state = 'NONE'
        user.save()
        reply =  u'居然没有添加【%s】题库！总么回事！' % real_course_name(course_name)
        return reply
    question_set = Question.objects.filter(course = current_course)
    if len(question_set) == 0:
        user.state = 'NONE'
        user.save()
        reply =  u'【%s】题库中还没有添加题目哦！' % real_course_name(course_name)
    else:
        question = random.choice(question_set)
        question_id = question.id
        user.state = 'COURSE' + '_' + course_name + '_' + '_' + str(question_id)
        user.save()
        if (course_name == 'MS'):
            reply = [u'开始猜歌名啦!', u'现在在听第0首歌', question.content]
        else:
            reply = u'''【%s】第0题：\n''' % real_course_name(course_name)
            reply += u'''--------------------------\n%s\n--------------------------\n''' \
                     % mark_safe(question.content)
            reply += u'''[1].%s\n[2].%s\n[3].%s\n[4].%s''' % \
                     (mark_safe(question.choice1), mark_safe(question.choice2),
                      mark_safe(question.choice3), mark_safe(question.choice4))
    return reply


def text_questionhandler(user, content):
    state = user.state
    state_list = state.split('_')
    if state_list[1] != 'MS' and (content <= '0' or content >= '5'):
        return u'请回复1,2,3,4中的某一个来回答问题！'
    else:
        question = Question.objects.get(id = state_list[3])
        if content == question.answer:
            new_state_list = update_state(state_list)
            if len(new_state_list) == 0:
                user.state = 'NONE'
                user.save()
                rank = update_record(user, state_list)
                reply = u'你，你，你居然把【%s】题库刷完了！' % real_course_name(state_list[1])
                if (rank >= 0):
                    reply += u'\n当前排在【%s】排行榜第%d名！' % (real_course_name(state_list[1]), rank)
                return reply
            else:
                user.state = new_state_list[0] + '_' + new_state_list[1] + '_' \
                             + new_state_list[2] + '_' + new_state_list[3]
                user.save()
                new_question = Question.objects.get(id = new_state_list[3])
                question_number = len(new_state_list[2].split(',')) - 1
                if (new_state_list[1] == 'MS'):
                    reply = [u'猜对啦！上一首歌曲是%s' % content, u'现在在听第%d首歌' % question_number, new_question.content]
                else:
                    reply = u'''回答正确！\n第%d题：\n''' % question_number
                    reply += u'''--------------------------\n%s\n--------------------------\n''' \
                             % mark_safe(new_question.content)
                    reply += u'''[1].%s\n[2].%s\n[3].%s\n[4].%s''' \
                             % (mark_safe(new_question.choice1), mark_safe(new_question.choice2),
                                mark_safe(new_question.choice3), mark_safe(new_question.choice4))
                return reply
        else:
            user.state = 'NONE'
            user.save()
            question_number = len(state_list[2].split(',')) - 1
            rank = update_record(user, state_list)
            if (state_list[1] == 'MS'):
                reply = u'''回答错误！猜歌名结束,共猜对%d首歌！''' % question_number
            else:
                reply = u'''回答错误！【%s】答题结束,共答对%d道题！''' % (real_course_name(state_list[1]), question_number)
            if (rank >= 0):
                    reply += u'\n当前排在【%s】排行榜第%d名！' % (real_course_name(state_list[1]), rank)
            return reply


def update_state(state_list):
    state_list[2] += state_list[3] + ','
    current_course = Course.objects.get(name = state_list[1])
    question_set = Question.objects.filter(course = current_course)
    answered_question = state_list[2].split(',')
    for i in range(0, len(answered_question) - 1):
        question_set = question_set.exclude(id = answered_question[i])
    if len(question_set) == 0:
        return []
    else:
        question = random.choice(question_set)
        state_list[3] = str(question.id)
    return state_list


def update_record(user, state_list):
    question_number = len(state_list[2].split(',')) - 1
    current_course = Course.objects.get(name = state_list[1])
    course_record = CoursesRecord.objects.filter(course = current_course)
    player_record = course_record.filter(player = user)
    if player_record:
        if player_record[0].score < question_number:
            player_record[0].score = question_number
            player_record[0].save()
    else:
        new_player_record = CoursesRecord(player = user, course = current_course, score = question_number)
        new_player_record.save()
    ordered_record = course_record.order_by('-score')
    for i in range(0, min(len(ordered_record), 6)):
        if (ordered_record[i].player == user):
            return i
    return -1




