# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)
    exercise_num = models.IntegerField(default=0)
    introduction = models.CharField(max_length=255,default='no introduction')
    def __unicode__(self):
        return self.name

class Question(models.Model):
    course = models.ForeignKey(Course)
    content = models.CharField(max_length=255,default='question')
    choice1 = models.CharField(max_length=255,default='choice1')
    choice2 = models.CharField(max_length=255,default='choice2')
    choice3 = models.CharField(max_length=255,default='choice3')
    choice4 = models.CharField(max_length=255,default='choice4')
    answer = models.CharField(max_length=255)
    answer_times = models.IntegerField(default=0)
    answer_correct_times = models.IntegerField(default=0)
    contributor = models.CharField(max_length=255,default='children')
    def __unicode__(self):
        if (self.course.name == 'MS'):
            return str(self.id) + '.' + self.answer
        else:
            return str(self.id) + '.' + self.content

class Player(models.Model):
    uid = models.CharField(max_length=255,default="")
    nickname = models.CharField(max_length=255,default="")
    state = models.CharField(max_length=255, default='none')  #0:不答题,1：答课程题目,2：猜数字, 3:
    def __unicode__(self):
        if self.nickname == '':
            return 'anonymous'
        else:
            return self.nickname

class CoursesRecord(models.Model):
    player = models.ForeignKey(Player)
    course = models.ForeignKey(Course)
    score = models.IntegerField(default=0)
    def __unicode__(self):
        return '%s in %s' % (self.player, self.course)



class QuestionsRecord(models.Model):
    player = models.ForeignKey(Player)
    question = models.ForeignKey(Question)
    state = models.IntegerField()
    def __unicode__(self):
        return '%s in %s' % (self.player, self.question)
