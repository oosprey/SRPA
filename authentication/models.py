#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:09
# Last modified: 2017-09-14 09:52
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User as _User

from . import USER_IDENTITIES, USER_IDENTITY_UNSET
from . import POLITICAL_STATUS, TEACHER_TITLE
from . import INSTITUTES, EDUCATION_BACKGROUNDS, EDUCATION_NONE


class UserInfo(models.Model):
    user = models.OneToOneField(_User, verbose_name='用户',
                                on_delete=models.CASCADE,
                                related_name='user_info')
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    identity = models.IntegerField(verbose_name='身份',
                                   choices=USER_IDENTITIES,
                                   default=USER_IDENTITY_UNSET)
    phone = models.CharField(verbose_name='联系电话', max_length=20)

    class Meta:
        verbose_name = '基本信息'
        verbose_name_plural = '基本信息'
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.user.first_name


class StudentInfo(UserInfo):
    user_info = models.OneToOneField(UserInfo, verbose_name='基本信息',
                                     on_delete=models.CASCADE,
                                     parent_link=True,
                                     related_name='student_info')
    student_id = models.CharField(verbose_name='学号', max_length=20)
    institute = models.CharField(verbose_name='学院', max_length=10,
                                 choices=INSTITUTES,
                                 default=INSTITUTES[0][0])

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'
        default_permissions = ('add', 'delete', 'update', 'view')


class TeacherInfo(UserInfo):
    user_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE,
                                     parent_link=True,
                                     related_name='teacher_info')
    title = models.IntegerField(verbose_name='职务',
                                choices=TEACHER_TITLE,
                                default=TEACHER_TITLE[0][0])

    class Meta:
        verbose_name = '指导教师信息'
        verbose_name_plural = '指导教师信息'
        default_permissions = ('add', 'delete', 'update', 'view')
