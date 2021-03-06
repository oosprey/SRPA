#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-04 13:38
# Last modified: 2017-10-04 15:51
# Filename: forms.py
# Description:
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from ProjectApproval.models import Project
from ProjectApproval.models import SocialInvitation


class ActivityForm(ModelForm):
    comment = forms.CharField(
        label=_('Comment'),
        widget=forms.Textarea(attrs={"rows": 3}))
    content = forms.CharField(
        label=_('Project Content'),
        widget=forms.Textarea(attrs={"rows": 3}))
    activity_time_from = forms.DateTimeField(
        label=_('Activity Time From'),
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form_datetime_hour form-control'},
            format='%Y-%m-%d %H:00:00'),
        required=False)
    activity_time_to = forms.DateTimeField(
        label=_('Activity Time To'),
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form_datetime_hour form-control'},
            format='%Y-%m-%d %H:00:00'),
        required=False)
    has_social = forms.BooleanField(
        label=_('Has Social'),
        widget=forms.CheckboxInput(attrs={}), required=False)
    contact_info = forms.CharField(
        label=_('Contact Info'),
        widget=forms.TextInput(),
        min_length=11,
        max_length=11)

    class Meta:
        model = Project
        fields = ['title', 'workshop', 'activity_time_from',
                  'activity_time_to', 'site', 'form', 'charger',
                  'contact_info', 'activity_range', 'amount', 'has_social',
                  'comment', 'attachment', 'content', 'contact_info']

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()
        errors = {}
        t1 = cleaned_data.get('activity_time_from')
        t2 = cleaned_data.get('activity_time_to')
        if t2 <= t1:
            if 'activity_time_to' in errors:
                errors['activity_time_to'].append(
                    _('Activity Time To should be '
                      'later than Activity Time From'))
            else:
                errors['activity_time_to'] = [
                    _('Activity Time To should be '
                      'later than Activity Time From')]
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class SocialInvitationForm(ModelForm):

    target_uid = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control'}))
    socials_info = forms.CharField(
        label=_('Social List'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    attend_info = forms.CharField(
        label=_('Social Attend Info'),
        widget=forms.Textarea(attrs={
            'class': 'form-control social_info', 'rows': 3}))
    ideology_info = forms.CharField(
        label=_('Social Ideology Info'),
        widget=forms.Textarea(attrs={
            'class': 'form-control social_info', 'rows': 3}))

    class Meta:
        model = SocialInvitation
        fields = ['target_uid', 'socials_info', 'attend_info', 'ideology_info']
