#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:11
# Last modified: 2017-09-07 09:11
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models

from authentication.models import User
from . import BILL_TYPES, EXPENSE_STATUSES


class BillSheet(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    created = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    user = models.ForeignKey(User, verbose_name='申报人')
    count = models.IntegerField(verbose_name='总单据数')
    amount = models.FloatField(verbose_name='总金额')
    status = models.IntegerField(verbose_name='报销单状态', choices=EXPENSE_STATUSES)

    class Meta:
        verbose_name = '报销单'
        verbose_name_plural = '报销单'
        ordering = ['status', 'created']
        permissions = (
            ('view_billsheet', '查看报销单'),
        )

    def __str__(self):
        return '%s %s(%d张发票，总共%d元)' % (
            self.created.today(), self.user.auth.first_name,
            self.count, self.amount)

    def save(self, *args, **kwargs):
        bill_infos = self.billinfo_set.all()
        self.count = sum([x.count for x in bill_infos])
        self.amount = sum([x.amount for x in bill_infos])
        super().save(*args, **kwargs)


class BillInfo(models.Model):
    sheet = models.ForeignKey(BillSheet, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    created = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    desc = models.CharField(verbose_name='详细说明', max_length=200,
                            blank=True, default='')
    count = models.IntegerField(verbose_name=u'数量')
    amount = models.FloatField(verbose_name=u'金额')
    type = models.CharField(verbose_name='类别', choices=BILL_TYPES,
                            max_length=30)

    class Meta:
        verbose_name = '发票信息'
        verbose_name_plural = '发票信息'
        permissions = (
            ('view_billinfo', '查看发票信息'),
        )

    def __str__(self):
        return '%d张发票，总共%f元(说明:%s)' % (self.count, self.amount, self.desc)
