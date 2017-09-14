#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:10
# Last modified: 2017-09-14 10:49
# Filename: urls.py
# Description:
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm


info_update_patterns = [
    url('^student/(?P<uid>.+)$', views.StudentInfoUpdate.as_view(),
        name='student'),
]


info_patterns = [
    url('^student/(?P<uid>.+)$', views.StudentInfoDetail.as_view(),
        name='student'),
    url('^update/', include(info_update_patterns, namespace='update')),
]

register_patterns = [
    url('^$', views.StudentRegisterView.as_view(),
        name='index'),
]

urlpatterns = [
    url('^captcha/refresh/', views.CaptchaRefresh.as_view(),
        name='captcha_refresh'),
    url('^login/', auth_views.LoginView.as_view(
        template_name='authentication/login.html',
        form_class=LoginForm), name='login'),
    url('^logout/', auth_views.LogoutView.as_view(next_page='index'),
        name='logout'),
    url('^register/', include(register_patterns, namespace='register')),
    url('^info/', include(info_patterns, namespace='info')),
]
