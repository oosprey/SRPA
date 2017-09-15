#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-14 14:39
# Last modified: 2017-09-15 14:51
# Filename: forms.py
# Description:
from django import forms


class DateForm(forms.Form):
    date = forms.DateField(
        label='日期',
        widget=forms.TextInput(attrs={
            'readonly':'true',
            'class': 'form-control'}))
