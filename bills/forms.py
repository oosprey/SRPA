#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:11
# Last modified: 2017-09-07 09:11
# Filename: forms.py
# Description:
from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.core.exceptions import ValidationError

from .models import BillInfo, BillSheet
from tools.utils import parse_utc


class BillInfoForm(ModelForm):
    class Meta:
        model = BillInfo
        fields = ['type', 'count', 'amount', 'desc']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'count': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BillSheetSearchForm(forms.Form):
    start_dt = forms.CharField(label='开始日期', widget=forms.DateTimeInput(
        attrs={'class': 'datetimepicker form-control'}), required=False)
    end_dt = forms.CharField(label='结束日期', widget=forms.DateTimeInput(
        attrs={'class': 'datetimepicker form-control'}), required=False)
    student_name = forms.CharField(label='姓名', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    student_id = forms.CharField(label='学号', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        try:
            cleaned_data['start_dt'] = parse_utc(cleaned_data['start_dt'])
            cleaned_data['end_dt'] = parse_utc(cleaned_data['end_dt'])
        except Exception:
            raise forms.ValidationError('请验证时间格式')
        if not any(cleaned_data.values()):
            raise forms.ValidationError('请至少输入一个检索关键字')
        return cleaned_data


BillInfoMultiForm = modelformset_factory(
    BillInfo, form=BillInfoForm, extra=0, min_num=1)
