#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 19:21
# Last modified: 2017-09-15 15:06
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

from const.models import Site, Workshop
from . import RESERVATION_STATUS, RESERVATION_SUBMITTED


class Reservation(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, verbose_name='预约人',
                             on_delete=models.CASCADE)
    site = models.ForeignKey(Site, verbose_name='场地',
                             on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, verbose_name='工坊',
                                 on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='状态',
                                 choices=RESERVATION_STATUS,
                                 default=RESERVATION_SUBMITTED)
    title = models.CharField(verbose_name='活动内容', max_length=100)
    activity_time_from = models.DateTimeField(verbose_name='活动开始时间')
    activity_time_to = models.DateTimeField(verbose_name='活动结束时间')
    reservation_time = models.DateTimeField(verbose_name='预约时间',
                                            auto_now_add=True)
    comment = models.TextField(verbose_name='备注')

    class Meta:
        verbose_name = '活动场地预约'
        verbose_name_plural = '活动场地预约'
        default_permissions = ('add', 'delete', 'update', 'view')
