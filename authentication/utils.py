#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 17:38
# Last modified: 2017-09-08 16:21
# Filename: utils.py
# Description:
from django.http import Http404

from .import USER_IDENTITY_STUDENT, USER_IDENTITY_SOCIAL


def get_detail_info_or_404(user_info):
    if user_info.identity == USER_IDENTITY_STUDENT:
        info = user_info.student_info
    elif user_info.identity == USER_IDENTITY_SOCIAL:
        info = user_info.social_info
    else:
        raise Http404()
    return info
