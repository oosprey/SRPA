#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 10:01
# Last modified: 2017-09-08 15:45
# Filename: context_processors.py
# Description:
from django.conf import settings as sys_settings

from authentication import USER_IDENTITY_STUDENT, USER_IDENTITY_SOCIAL


def expose_settings(request):
    settings = {
        'TITLE': sys_settings.TITLE,
        'USER_IDENTITY_STUDENT': USER_IDENTITY_STUDENT,
        'USER_IDENTITY_SOCIAL': USER_IDENTITY_SOCIAL,
    }
    return settings
