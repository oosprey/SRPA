#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:13
# Last modified: 2017-09-07 22:04
# Filename: utils.py
# Description:
from django.core.exceptions import PermissionDenied
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from guardian.shortcuts import assign_perm, remove_perm


def assign_perms(name, user_or_group, perms=None, obj=None):
    if perms is None:
        perms = ['add', 'change', 'delete', 'view']
    perms = [perm + '_' + name for perm in perms]
    for perm in perms:
        assign_perm(perm, user_or_group, obj)


def remove_perms(name, user_or_group, perms=None, obj=None):
    if perms is None:
        perms = ['add', 'change', 'delete', 'view']
    perms = [perm + '_' + name for perm in perms]
    for perm in perms:
        remove_perm(perm, user_or_group, obj)


def check_perm(perm, user, obj, raise_403=True):
    if user.has_perm(perm, obj):
        return True
    elif raise_403:
        raise PermissionDenied()
    else:
        return False


def parse_utc(dt, tz=None):
    if not dt:
        return dt
    dt_obj = parse_datetime(dt)
    return make_aware(dt_obj, timezone=tz)
