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
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from ProjectApproval import PROJECT_STATUS, PROJECT_SUBMITTED
from ProjectApproval.forms import ActivityForm
from ProjectApproval.models import Project
from const.models import Workshop
from authentication.models import UserInfo
from authentication import USER_IDENTITIES
from ProjectApproval import PROJECT_STATUS_CAN_EDIT


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class ProjectBase(LoginRequiredMixin):
    """
    A base view for all project actions. SHOULD NOT DIRECTLY USE THIS.
    """
    model = Project


class ProjectIndex(ProjectBase, TemplateView):

    template_name = "ProjectApproval/index.html"


class ProjectList(ProjectBase, ListView):
    """
    A view for displaying user-related projects list. GET only.
    """
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ProjectDetail(ProjectBase, DetailView):
    """
    A view for displaying specified project. GET only.

    """
    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class ProjectAdd(ProjectBase, CreateView):
    """
    A view for creating a new project.
    """
    template_name = 'ProjectApproval/project_add.html'
    form_class = ActivityForm
    success_url = reverse_lazy('project:index')
    form_post_url = 'project:ordinary:add'

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.success_url
        return super(CreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})


class ProjectUpdate(ProjectBase, UpdateView):
    """
    A view for updating an exist project. Should check status before
    change, reject change if not match specified status.
    """
    template_name = 'ProjectApproval/project_update.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = ActivityForm
    success_url = reverse_lazy('project:index')
    form_post_url = 'project:ordinary:update'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_ajax = request.is_ajax()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_EDIT
        if not is_ajax or not allowed_status:
            return HttpResponseForbidden()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_EDIT
        if not allowed_status:
            return HttpResponseForbidden()
        return super(ProjectUpdate, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['back_url'] = self.success_url
        kwargs['form_post_url'] = self.form_post_url
        return super(UpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return JsonResponse({'status': 0, 'redirect': self.success_url})
