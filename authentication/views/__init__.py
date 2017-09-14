#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:15
# Last modified: 2017-09-14 10:06
# Filename: __init__.py
# Description:
from .auth import IndexView, CaptchaRefresh
from .auth import StudentRegisterView
from .info_detail import StudentInfoDetail
from .info_update import StudentInfoUpdate

__all__ = [
    'IndexView', 'CaptchaRefresh'
    'StudentRegisterView',
    'StudentInfoDetail', 'SocialInfoDetail',
    'StudentInfoUpdate', 'SocialInfoUpdate',
]
