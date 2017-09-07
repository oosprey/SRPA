#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:14
# Last modified: 2017-09-07 17:41
# Filename: filters.py
# Description:
from django import template


register = template.Library()


@register.filter('addcls')
def addcls(field, cls):
    return field.as_widget(attrs={"class": cls})
