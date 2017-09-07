#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:12
# Last modified: 2017-09-07 09:12
# Filename: utils.py
# Description:
from django.core.exceptions import PermissionDenied

from . import ESTATUS_SUBMIT, ESTATUS_AMEND


def check_edit_status(obj, raise_403=True):
    if obj.status == ESTATUS_SUBMIT or obj.status == ESTATUS_AMEND:
        return True
    elif raise_403:
        raise PermissionDenied()
    else:
        return False
