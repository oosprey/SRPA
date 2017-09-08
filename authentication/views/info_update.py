#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:06
# Last modified: 2017-09-08 22:05
# Filename: info_update.py
# Description:
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from guardian.mixins import PermissionRequiredMixin

from authentication.models import SocialInfo, StudentInfo


class InfoUpdateBase(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    A base view for updaing info.
    """

    template_name = 'authentication/update_info.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True

    def get_success_url(self):
        slug_val = getattr(self.object, self.slug_field)
        return reverse_lazy(self.success_url, args=(slug_val,))

    def get(self, request, *args, **kwargs):
        slug_val = getattr(request.user.user_info, self.slug_field)
        self.success_url = reverse_lazy(self.success_url, args=(slug_val,))
        return super(InfoUpdateBase, self).get(request, *args, **kwargs)


class StudentInfoUpdate(InfoUpdateBase):
    """
    A view for updaing student info.
    """

    model = StudentInfo
    fields = ['student_id', 'institute']
    success_url = 'info:student'
    permission_required = 'update_studentinfo'


class SocialInfoUpdate(InfoUpdateBase):
    """
    A view for updaing social info.
    """

    model = SocialInfo
    fields = ['citizen_id', 'title', 'education',
              'political_status']
    success_url = 'info:social'
    permission_required = 'update_socialinfo'
