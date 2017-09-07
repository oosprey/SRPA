#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 20:01
# Last modified: 2017-09-07 20:01
# Filename: admin.py
# Description:
from django.contrib import admin

from .models import Site, Workshop


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    pass
