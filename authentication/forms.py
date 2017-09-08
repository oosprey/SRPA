#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:09
# Last modified: 2017-09-08 17:22
# Filename: forms.py
# Description:
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import UserInfo, StudentInfo, SocialInfo
from const.models import CaptchaField


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()


class RegisterForm(ModelForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput())
    name = forms.CharField(
        label='姓名',
        widget=forms.TextInput())
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(),
        min_length=1,
        max_length=20)
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(),
        min_length=1,
        max_length=20)
    captcha = CaptchaField()

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'confirm_password',
                  'name', 'phone', 'captcha']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        errors = {}
        username = cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            errors['username'] = [_('该用户名已存在')]
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            errors['confirm_password'] = [_('请确认两次输入密码一致')]
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class StudentRegisterForm(RegisterForm):
    class Meta:
        model = StudentInfo
        fields = ['username', 'password', 'confirm_password',
                  'name', 'phone', 'student_id', 'institute', 'captcha']


class SocialRegisterForm(RegisterForm):
    class Meta:
        model = SocialInfo
        fields = ['username', 'password', 'confirm_password',
                  'name', 'phone', 'citizen_id', 'title', 'education',
                  'political_status', 'captcha']
