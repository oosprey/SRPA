#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:17
# Last modified: 2017-10-04 15:46
# Filename: admin.py
# Description:
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DetailView
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin

from const.forms import FeedBackForm
from const.models import FeedBack
from ProjectApproval.models import Project
from ProjectApproval import PROJECT_STATUS_CAN_CHECK, PROJECT_SUBMITTED
from ProjectApproval import PROJECT_APPROVED, PROJECT_EDITTING
from ProjectApproval import PROJECT_TERMINATED, PROJECT_STATUS_CAN_FINISH
from ProjectApproval import PROJECT_FINISHED, PROJECT_END_EDITTING
from authentication import USER_IDENTITY_TEACHER


class AdminProBase(UserPassesTestMixin):

    model = Project
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and\
            user.user_info.identity == USER_IDENTITY_TEACHER


class AdminProjectList(AdminProBase, PermissionListMixin, ListView):
    """
    A view for displaying projects list for admin. GET only.
    """
    model = Project
    paginate_by = 12
    ordering = ['status', '-apply_time']
    raise_exception = True
    permission_required = 'view_project'

    def get_queryset(self):
        return super(AdminProjectList, self).get_queryset().filter(
            workshop__group__in=self.request.user.groups.all())


class AdminProjectDetail(AdminProBase, PermissionRequiredMixin, DetailView):
    """
    A view for displaying specified project for admin. GET only.
    """
    model = Project
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True
    permission_required = 'view_project'

    def get_context_data(self, **kwargs):
        feed = FeedBack.objects.filter(
            target_uid=self.object.uid)
        form = FeedBackForm({'target_uid': self.object.uid})
        kwargs['budgets'] = [x.strip().split(' ') for x in
                             self.object.budget.split('\n')]
        kwargs['feed'] = feed
        kwargs['form'] = form
        return super(AdminProjectDetail, self).get_context_data(**kwargs)


class AdminProjectUpdate(AdminProBase, PermissionRequiredMixin, UpdateView):
    """
    A view for admin to update an exist project.
    Should check status before change, reject change if not match
    specified status.
    """
    http_method_names = ['post']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = FeedBackForm
    raise_exception = True
    permission_required = 'update_project'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_CHECK or\
            self.object.status in PROJECT_STATUS_CAN_FINISH
        if not allowed_status:
            return HttpResponseForbidden()
        return super(AdminProjectUpdate, self).post(request, *args,
                                                    **kwargs)

    def get_form_kwargs(self):
        return {'data': self.request.POST}

    def form_valid(self, form):
        obj = self.object
        feedback = form.save(commit=False)
        if obj.uid != feedback.target_uid:
            # Mismatch target_uid
            return JsonResponse({'status': 2, 'reason': _('Illegal Input')})
        feedback.user = self.request.user
        status = form.cleaned_data['status']
        if obj.status not in PROJECT_STATUS_CAN_CHECK and\
                obj.status not in PROJECT_STATUS_CAN_FINISH:
            return JsonResponse({
                'status': 2, 'reason': _('Illegal Input')})
        if status == 'APPROVE':
            obj.status = PROJECT_APPROVED if obj.status in\
                PROJECT_STATUS_CAN_CHECK else PROJECT_FINISHED
        elif status == 'EDITTING':
            obj.status = PROJECT_EDITTING if obj.status in\
                PROJECT_STATUS_CAN_CHECK else PROJECT_END_EDITTING
        elif status == 'TERMINATED':
            if obj.status in PROJECT_STATUS_CAN_CHECK:
                obj.status = PROJECT_TERMINATED
            elif obj.status in PROJECT_STATUS_CAN_FINISH:
                return JsonResponse({
                    'status': 2, 'reason': _('Illegal Input')})
        obj.save()
        feedback.save()
        return JsonResponse({'status': 0})

    def form_invalid(self, form):
        return JsonResponse({'status': 1, 'reason': _('Illegal Input')})
