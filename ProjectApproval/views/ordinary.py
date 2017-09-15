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
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse, NoReverseMatch
from django.http import HttpResponseRedirect

from ProjectApproval import PROJECT_STATUS, PROJECT_SUBMITTED
from ProjectApproval.forms import AddActivityForm
from ProjectApproval.models import Project
from const.models import Workshop
from authentication.models import TeacherInfo


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
    # template_name = 'ProjectApproval/index.html'
    pass


class ProjectList(ProjectBase, ListView):
    """
    A view for displaying user-related projects list. GET only.
    """
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs['origin'] = 'List'
        return super(ListView, self).get_context_data(**kwargs)


class ProjectDetail(ProjectBase, DetailView):
    """
    A view for displaying specified project. GET only.
    """    
    http_method_names = ['get']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True
    fields = ['student_id', 'institute']
    template_name = 'authentication/student_info_detail.html'
    permission_required = 'view_studentinfo'


class ProjectAdd(ProjectBase, CreateView):
    """
    A view for creating a new project.
    """
    # template_name = 'ProjectApproval/add_activity.html'
    form_class = AddActivityForm
    success_url = reverse_lazy('project:ordinary:list')
    form_post_url = reverse_lazy('project:ordinary:add')

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.success_url
        kwargs['origin'] = 'Add'
        return super(CreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdate(ProjectBase, UpdateView):
    """
    A view for updating an exist project. Should check status before
    change, reject change if not match specified status.
    """

    template_name = 'ProjectApproval/project_update.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True
    fields = ['title', 'workshop', 'activity_time_from',
                  'activity_time_to', 'site', 'form', 'charger',
                  'contact_info', 'activity_range', 'amount', 'has_social',
                  'budget', 'comment', 'instructor_comment',
                  'attachment']
    success_url = 'project:ordinary:list'
    permission_required = 'update_studentinfo'       
    def get_success_url(self):
        slug_val = getattr(self.object, self.slug_field)
        return reverse_lazy(self.success_url)
				                                                                                
    def get(self, request, *args, **kwargs):
        slug_val = getattr(request.user.user_info, self.slug_field)
        self.success_url = reverse_lazy(self.success_url)
        return super(ProjectUpdate, self).get(request, *args, **kwargs)

