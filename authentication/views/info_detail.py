#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:06
# Last modified: 2017-09-08 22:05
# Filename: info_detail.py
# Description:
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from guardian.mixins import PermissionRequiredMixin

from authentication.models import SocialInfo, StudentInfo


class InfoDetailBase(PermissionRequiredMixin, DetailView):
    """
    A base view for displaying detail info.
    """

    http_method_names = ['get']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True


class StudentInfoDetail(InfoDetailBase):
    """
    A view for displaying student info.
    """

    model = StudentInfo
    fields = ['student_id', 'institute']
    template_name = 'authentication/student_info_detail.html'
    permission_required = 'view_studentinfo'


class SocialInfoDetail(InfoDetailBase):
    """
    A view for displaying social info.
    """

    model = SocialInfo
    fields = ['citizen_id', 'title', 'education',
              'political_status']
    template_name = 'authentication/social_info_detail.html'
    permission_required = 'view_socialinfo'
