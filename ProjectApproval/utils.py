#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:49
# Last modified: 2017-09-09 10:06
# Filename: utils.py
# Description:
import os.path as osp

from datetime import datetime


def get_user_project_attachments_path(instance, filename):
    now = datetime.now()
    return 'project_attachments/{}/{:04d}/{:02d}/{:02d}/{}'.format(
        instance.user.id, now.year, now.month, now.day, filename)
