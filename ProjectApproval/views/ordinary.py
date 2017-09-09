#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:17
# Last modified: 2017-09-09 10:08
# Filename: ordinary.py
# Description:
from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ProjectApproval.models import Project


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class ProjectBase(LoginRequiredMixin):
    """
    A base view for all project actions. SHOULD NOT DIRECTLY USE THIS.
    """

    model = Project


class ProjectRedirect(ProjectBase, RedirectView):
    """
    A view for redirect admin users and ordinary users.
    """

    pass


class ProjectList(ProjectBase, ListView):
    """
    A view for displaying user-related projects list. GET only.
    """

    pass


class ProjectDetail(ProjectBase, DetailView):
    """
    A view for displaying specified project. GET only.
    """

    pass


class ProjectAdd(ProjectBase, CreateView):
    """
    A view for creating a new project.
    """

    pass


class ProjectUpdate(ProjectBase, UpdateView):
    """
    A view for updating an exist project. Should check status before
    change, reject change if not match specified status.
    """

    pass
