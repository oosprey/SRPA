#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 08:48
# Last modified: 2017-09-14 14:42
# Filename: urls.py
# Description:
from django.conf.urls import url, include

from . import views


ord_patterns = [
    url(r'^list/$', views.ReservationList.as_view(), name='list'),
    url(r'^detail/$', views.ReservationDetail.as_view(), name='detail'),
    url(r'^add/$', views.ReservationAdd.as_view(), name='add'),
    url(r'^update/$', views.ReservationUpdate.as_view(),
        name='update'),
]

admin_patterns = [
    url(r'^list/$', views.AdminReservationList.as_view(), name='list'),
    url(r'^detail/$', views.AdminReservationDetail.as_view(), name='detail'),
    url(r'^update/$', views.AdminReservationUpdate.as_view(),
        name='update'),
]


urlpatterns = [
    url(r'^$', views.ReservationRedirect.as_view(), name='index'),
    url(r'^status/', views.ReservationStatus.as_view(), name='status'),
    url(r'^ordinary/', include(ord_patterns, namespace='ordinary')),
    url(r'^admin/', include(admin_patterns, namespace='admin')),
]
