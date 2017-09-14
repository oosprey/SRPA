#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:17
# Last modified: 2017-09-09 10:08
# Filename: admin.py
# Description:
from django.contrib.auth.mixins import LoginRequiredMixin

from .ordinary import ProjectList, ProjectUpdate, ProjectDetail


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class AdminProjectBase(LoginRequiredMixin):
    """
    A base view for all project actions. SHOULD NOT DIRECTLY USE THIS.
    """

    pass


class AdminProjectList(AdminProjectBase, ProjectList):
    """
    A view for displaying projects list for admin. GET only.
    """

    pass


class AdminProjectDetail(AdminProjectBase, ProjectDetail):
    """
    A view for displaying specified project for admin. GET only.
    """
    
    pass


class AdminProjectUpdate(AdminProjectBase, ProjectUpdate):
    """
    A view for admin to update an exist project.
    Should check status before change, reject change if not match
    specified status.
    """

    pass
