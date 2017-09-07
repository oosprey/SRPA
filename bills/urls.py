#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:12
# Last modified: 2017-09-07 09:12
# Filename: urls.py
# Description:
from django.conf.urls import url, include

from . import views
from . import admin_views


bill_sheet_patterns = [
    url(r'^create/$', views.BillsSheetCreate.as_view(), name='bills_sheet_create'),
    url(r'^list/', views.BillsSheetList.as_view(), name='bills_sheet_list'),
    url(r'^detail/(?P<uid>.+)/$', views.BillsSheetDetail.as_view(), name='bills_sheet_detail'),
    url(r'^update/(?P<uid>.+)/$', views.BillsSheetUpdate.as_view(), name='bills_sheet_update'),
    url(r'^delete/', include([
        url(r'^$', views.BillsSheetDelete.as_view(), name='bills_sheet_delete'),
        url(r'^(?P<uid>.+)$', views.BillsSheetDelete.as_view(), name='bills_sheet_delete')])),
]

admin_bill_sheet_patterns = [
    url(r'^list/', admin_views.AdminBillsSheetList.as_view(), name='bills_sheet_list'),
    url(r'^stats/$', admin_views.AdminBillsSheetStatistic.as_view(), name='bills_sheet_statistic'),
    url(r'^detail/(?P<uid>.+)/$', admin_views.AdminBillsSheetDetail.as_view(), name='bills_sheet_detail'),
    url(r'^update/(?P<uid>.+)/$', admin_views.AdminBillsSheetDetail.as_view(), name='bills_sheet_update'),
]


admin_urlpatterns = [
    url(r'^$', admin_views.AdminBillsSheetList.as_view()),
    url(r'^bill_sheet/', include(admin_bill_sheet_patterns)),
]


urlpatterns = [
    url(r'^$', views.BillsSheetList.as_view()),
    url(r'^bill_sheet/', include(bill_sheet_patterns)),
    url(r'^bill_info/delete/(?P<uid>.+)/$', views.BillsInfoDelete.as_view(), name='bills_info_delete'),
    url(r'^admin/', include(admin_urlpatterns, namespace='expense_admin')),
]
