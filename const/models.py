#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 18:34
# Last modified: 2017-09-14 09:46
# Filename: models.py
# Description:
from uuid import uuid4

from django.db import models
from captcha.fields import CaptchaField as _CaptchaField

from authentication.models import TeacherInfo


class Site(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name='场地', max_length=50)

    class Meta:
        verbose_name = '场地信息'
        verbose_name_plural = '场地信息'
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.desc


class Workshop(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name='工坊', max_length=50)
    instructor = models.ForeignKey(TeacherInfo, verbose_name='指导教师',
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = '工坊信息'
        verbose_name_plural = '工坊信息'
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.desc


class CaptchaField(_CaptchaField):
    def __init__(self, *args, **kwargs):
        super(CaptchaField, self).__init__(*args, **kwargs)
        self.label = '验证码'
