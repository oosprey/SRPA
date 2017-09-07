#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-06-10 15:41
# Last modified: 2017-06-12 09:37
# Filename: admin_views.py
# Description:
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import BaseFormView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.db.models import Q
from django.utils.http import urlencode

from authentication import USER_LEVEL_A

from . import ESTATUS_TYPES, BILL_TYPES, _BILL_TYPES_DESC
from .views import BillsSheetList, BillsSheetDetail
from .models import BillInfo
from .forms import BillSheetSearchForm


class AdminPermissionRequired(LoginRequiredMixin, PermissionRequiredMixin):
    def has_permission(self):
        # Test if user has high authority
        if self.request.user.user.level >= USER_LEVEL_A:
            return True
        else:
            raise PermissionDenied()


class AdminBillsSheetList(AdminPermissionRequired, BillsSheetList):
    def get_queryset(self):
        return super(BillsSheetList, self).get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_admin'] = True
        context['search_form'] = BillSheetSearchForm
        return context

    def get(self, request, *args, **kwargs):
        form = BillSheetSearchForm(request.GET)
        query = Q()
        args = ''
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['start_dt']:
                query &= Q(created__gte=cleaned_data['start_dt'])
            if cleaned_data['end_dt']:
                query &= Q(created__lte=cleaned_data['end_dt'])
            if cleaned_data['student_id']:
                query &= Q(user__student_id__startswith=cleaned_data['student_id'])
            if cleaned_data['student_name']:
                query &= Q(user__auth__first_name__startswith=cleaned_data['student_name'])
            args = urlencode(cleaned_data)
        self.queryset = self.model._default_manager.filter(query)
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['args'] = args
        return self.render_to_response(context)


class AdminBillsSheetDetail(AdminPermissionRequired, BillsSheetDetail):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        status = int(request.POST.get('status', -1))
        if status not in ESTATUS_TYPES:
            raise PermissionDenied()
        self.object.status = status
        self.object.save()
        return self.render_to_response(self.get_context_data(**kwargs))


class AdminBillsSheetStatistic(AdminPermissionRequired, BaseFormView, ListView):
    model = BillInfo
    paginate_by = 10
    template_name = 'bills/billsheet_statistic.html'
    form_class = BillSheetSearchForm
    success_template_name = 'bills/widgets/statistic_table.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        stat_dict = {}
        for idx, (bill_type, type_display) in enumerate(BILL_TYPES):
            stat_dict[bill_type] = {}
            stat_dict[bill_type]['idx'] = idx
            stat_dict[bill_type]['display'] = type_display
            stat_dict[bill_type]['desc'] = _BILL_TYPES_DESC[idx]
            stat_dict[bill_type]['count'] = 0
            stat_dict[bill_type]['amount'] = 0
        for obj in self.object_list:
            stat_dict[obj.type]['count'] += obj.count
            stat_dict[obj.type]['amount'] += obj.amount
        stats = list(stat_dict.items())
        stats.sort(key=lambda x: x[1]['idx'])
        context['stats'] = stats
        context['search_form'] = BillSheetSearchForm()
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        query = Q()
        if cleaned_data['start_dt']:
            query &= Q(created__gte=cleaned_data['start_dt'])
        if cleaned_data['end_dt']:
            query &= Q(created__lte=cleaned_data['end_dt'])
        if cleaned_data['student_id']:
            query &= Q(sheet__user__student_id__startswith=cleaned_data['student_id'])
        if cleaned_data['student_name']:
            query &= Q(sheet__user__auth__first_name__startswith=cleaned_data['student_name'])
        self.queryset = self.model._default_manager.filter(query)
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.response_class(
            request=self.request,
            template=self.success_template_name,
            context=context,
            using=self.template_engine,
            content_type=self.content_type
        )

    def form_invalid(self, form):
        self.object_list = []
        return self.render_to_response(self.get_context_data())
