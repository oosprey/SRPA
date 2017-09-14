#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-14 14:39
# Last modified: 2017-09-14 14:58
# Filename: forms.py
# Description:

from django import forms

from datetimewidget.widgets import DateWidget


class DateForm(forms.Form):
    date = forms.DateTimeField(
        widget=DateWidget(usel10n=True, bootstrap_version=3))
