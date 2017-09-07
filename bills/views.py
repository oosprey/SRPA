#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:12
# Last modified: 2017-09-07 09:13
# Filename: views.py
# Description:
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.http import Http404, JsonResponse
from django.core.exceptions import PermissionDenied

from . import _BILL_TYPES_DESC, DELETE_MSGS
from . import ESTATUS_SUBMIT, ESTATUS_AMEND, ESTATUS_REJECT, ESTATUS_APPROVE
from .models import BillSheet, BillInfo
from .forms import BillInfoMultiForm
from .utils import check_edit_status
from tools.utils import assign_perms, check_perm, remove_perms


class BillsSheetList(LoginRequiredMixin, ListView):
    model = BillSheet
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user__auth=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ESTATUS_SUBMIT'] = ESTATUS_SUBMIT
        context['ESTATUS_AMEND'] = ESTATUS_AMEND
        return context


class BillsSheetCreate(LoginRequiredMixin, CreateView):
    model = BillSheet
    template_name = 'bills/billsheet_edit.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = kwargs
        context['field_descriptions'] = _BILL_TYPES_DESC
        formset = BillInfoMultiForm(queryset=BillInfo.objects.none())
        context['formset'] = kwargs.pop('form', formset)
        return context

    def post(self, *args, **kwargs):
        self.object = None
        formset = BillInfoMultiForm(self.request.POST)
        user = self.request.user
        if formset.is_valid():
            bill_sheet = BillSheet.objects.create(
                user=user.user,
                count=0, amount=0,
                status=ESTATUS_SUBMIT)
            bill_infos = formset.save(commit=False)
            for bill_info in bill_infos:
                bill_info.sheet = bill_sheet
                bill_info.save()
            bill_sheet.save()
            assign_perms('billsheet', user, obj=bill_sheet)
            return redirect('bills_sheet_detail', permanent=True,
                            uid=bill_sheet.uid)
        else:
            return self.form_invalid(formset)


class BillsSheetDetail(LoginRequiredMixin, DetailView):
    model = BillSheet
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'].billinfos = context['object'].billinfo_set.all()
        context['ESTATUS_SUBMIT'] = ESTATUS_SUBMIT
        context['ESTATUS_AMEND'] = ESTATUS_AMEND
        context['ESTATUS_APPROVE'] = ESTATUS_APPROVE
        context['ESTATUS_REJECT'] = ESTATUS_REJECT
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        check_perm('view_billsheet', self.request.user, self.object)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class BillsSheetUpdate(LoginRequiredMixin, UpdateView):
    model = BillSheet
    fields = []
    template_name = 'bills/billsheet_edit.html'
    success_url = 'bills_sheet_detail'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        check_perm('change_billsheet', self.request.user, self.object)
        check_edit_status(self.object)
        context = kwargs
        bill_infos = self.object.billinfo_set.all()
        formset = BillInfoMultiForm(queryset=bill_infos)
        context['formset'] = formset
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        formset = BillInfoMultiForm(self.request.POST)
        if formset.is_valid():
            self.object = self.get_object()
            check_edit_status(self.object)
            check_perm('change_billsheet', self.request.user, self.object)
            for form in formset.forms:
                if not form.has_changed():
                    continue
                inst = form.save(commit=False)
                inst.sheet = self.object
                inst.save()
            self.object.save()
            uid = self.object.uid
            return redirect(reverse(self.success_url, kwargs={'uid': uid}))
        else:
            return self.form_invalid(formset)


class BillsInfoDelete(LoginRequiredMixin, DeleteView):
    model = BillInfo
    http_method_names = ['get']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self, *args, **kwargs):
        context = {}
        try:
            obj = self.get_object()
            sheet = obj.sheet
            check_perm('change_billsheet', self.request.user, sheet)
            check_edit_status(sheet)
            obj.delete()
            if sheet.billinfo_set.count() == 0:
                remove_perms('billsheet', self.request.user, obj=sheet)
                sheet.delete()
                sheet_deleted = True
            else:
                sheet.save()
                sheet_deleted = False
        except Http404:
            context['status'] = -1  # No such item
        else:
            context['status'] = 0  # Success
            context['redirect'] = reverse('bills_sheet_detail',
                                          kwargs={'uid': sheet.uid})
            if sheet_deleted:
                context['status'] = 1  # Success but sheet is now empty
                context['redirect'] = reverse('bills_sheet_list')
        context['msg'] = DELETE_MSGS[context['status']]
        return JsonResponse(context)


class BillsSheetDelete(LoginRequiredMixin, DeleteView):
    model = BillSheet
    http_method_names = ['post']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    success_url = reverse_lazy('bills_sheet_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        check_perm('change_billsheet', self.request.user, obj)
        check_edit_status(obj)
        remove_perms('billsheet', request.user, obj=obj)
        return super().delete(request, *args, **kwargs)
