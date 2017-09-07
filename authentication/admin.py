#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:09
# Last modified: 2017-09-07 17:36
# Filename: admin.py
# Description:
from django.contrib import admin

from .models import StudentInfo, SocialInfo, UserInfo


@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialInfo)
class SocialInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass