#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 18:34
# Last modified: 2017-09-07 20:01
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models


class Site(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name='场地', max_length=50)

    def __str__(self):
        return self.desc


class Workshop(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name='工坊', max_length=50)

    def __str__(self):
        return self.desc
