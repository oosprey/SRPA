#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:10
# Last modified: 2017-09-08 16:21
# Filename: urls.py
# Description:
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url('^accounts/login', views.LoginView.as_view(), name='login'),
    url('^accounts/logout', auth_views.LogoutView.as_view(next_page='login'),
        name='logout'),
    url('^accounts/register', views.RegisterView.as_view(),
        name='register'),
    url('^accounts/load_auth_form', views.AuthFormLoadView.as_view(),
        name='load_auth_form'),
    url('^accounts/student_register', views.StudentRegisterView.as_view(),
        name='student_register'),
    url('^accounts/social_register', views.SocialRegisterView.as_view(),
        name='social_register'),
    url('^accounts/update_detail_info/(?P<uid>.*)/$',
        views.DetailInfoUpdateView.as_view(), name='update_detail_info'),
    url('^accounts/detail_info', views.DetailInfoRedirectView.as_view(),
        name='detail_info'),
    url('^accounts/student_detail_info', views.StudentDetailInfoView.as_view(),
        name='student_detail_info'),
    url('^accounts/social_detail_info', views.SocialDetailInfoView.as_view(),
        name='social_detail_info'),
]
