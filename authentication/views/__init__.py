#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:15
# Last modified: 2017-09-08 20:18
# Filename: __init__.py
# Description:
from .auth import IndexView, CaptchaRefresh, AuthFormLoadView
from .auth import RegisterView, StudentRegisterView, SocialRegisterView
from .info_detail import StudentInfoDetail, SocialInfoDetail
from .info_update import StudentInfoUpdate, SocialInfoUpdate

__all__ = [
    'IndexView', 'CaptchaRefresh', 'AuthFormLoadView',
    'RegisterView', 'StudentRegisterView', 'SocialRegisterView',
    'StudentInfoDetail', 'SocialInfoDetail',
    'StudentInfoUpdate', 'SocialInfoUpdate',
]
