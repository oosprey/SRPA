#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:03
# Last modified: 2017-10-05 10:17
# Filename: ordinary.py
# Description:
from uuid import UUID
from datetime import datetime, timedelta, timezone

from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.views.generic import DetailView, TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.urls import reverse, NoReverseMatch
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin
from django import forms

from authentication import USER_IDENTITY_STUDENT
from authentication import USER_IDENTITY_ADMIN
from SiteReservation import RESERVATION_APPROVED, RESERVATION_CANCELLED
from SiteReservation import RESERVATION_SUBMITTED, RESERVATION_STATUS_CAN_EDIT
from SiteReservation.models import Reservation
from SiteReservation.forms import DateForm, ReservationForm
from SiteReservation.utils import is_conflict, export_reservation
from const.models import Site, FeedBack
from tools.utils import assign_perms


class ReservationBase(UserPassesTestMixin):
    """
    A base view for all reservation actions. SHOULD NOT DIRECTLY USE THIS.
    """
    model = Reservation
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and \
            user.user_info.identity == USER_IDENTITY_STUDENT


class ReservationIndex(TemplateView):
    template_name = 'SiteReservation/index.html'


class ReservationStatus(FormView):
    template_name = 'SiteReservation/reservation_status.html'
    status_table_name = 'SiteReservation/status_table.html'
    form_class = DateForm

    def get_context_data(self, **kwargs):
        kwargs['sites'] = Site.objects.all().order_by('desc')
        return super(ReservationStatus, self).get_context_data(**kwargs)

    def form_valid(self, form):
        uid = self.request.POST.get('site_uid', None)
        date = form.cleaned_data['date']
        if date < datetime.now().date():
            return JsonResponse({'status': 2,
                                 'reason': _('Please choose a future time')})
        start_dt = datetime.combine(date, datetime.min.time())
        start_dt = start_dt.replace(tzinfo=timezone.utc)
        end_dt = start_dt + timedelta(days=1)
        if not uid:
            raise Http404()
        try:
            uid = UUID(uid)
        except ValueError:
            return JsonResponse({'status': 3,
                                 'reason': _('Illegal Input')})
        site = get_object_or_404(Site, uid=uid)
        reservations = Reservation.objects.filter(site=site)
        reservations = reservations.filter(status=RESERVATION_APPROVED)
        reservations = reservations.filter(
            Q(activity_time_from__gte=start_dt) &
            Q(activity_time_from__lt=end_dt))
        available_status = [True for _ in range(14)]  # 0 -> 08:00 ~ 09:00
        for r in reservations:
            for hour in range(r.activity_time_from.hour,
                              r.activity_time_to.hour):
                available_status[hour] = False
        status_table = render_to_string(
            self.status_table_name, request=self.request,
            context={'available_status': available_status,
                     'date': date,
                     'site': site})
        return JsonResponse({'status': 0, 'html': status_table})

    def form_invalid(self, form):
        return JsonResponse({'status': 1, 'reason': _('Wrong form data, '
                                                      'Please check again')})


class ReservationList(ReservationBase, PermissionListMixin, ListView):
    """
    A view for displaying user-related reservations list. GET only.
    """
    permission_required = 'view_reservation'
    paginate_by = 10
    ordering = ['status', '-reservation_time']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ReservationCancel(ReservationBase, PermissionRequiredMixin, DetailView):
    """
    A view for displaying user-related reservations list after terminating.
    """
    raise_exception = True
    permission_required = 'view_reservation'
    success_url = reverse_lazy('reservation:index')
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = RESERVATION_CANCELLED
        self.object.save()
        return redirect(self.success_url)


class ReservationExport(ReservationBase, PermissionRequiredMixin, DetailView):
    """
    A view for exporting reservation application
    """
    raise_exception = True
    permission_required = 'view_reservation'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(export_reservation(self.object))


class ReservationDetail(ReservationBase, PermissionRequiredMixin, DetailView):
    """
    A view for displaying specified reservation. GET only.
    """
    raise_exception = True
    permission_required = 'view_reservation'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        feedbacks = FeedBack.objects.filter(target_uid=self.object.uid)
        feedbacks.order_by('-created')
        kwargs['feedbacks'] = feedbacks
        return super(ReservationDetail, self).get_context_data(**kwargs)


class ReservationAdd(ReservationBase, PermissionRequiredMixin, CreateView):
    """
    A view for creating a new reservation.
    """
    accept_global_perms = True
    raise_exception = True
    permission_required = 'SiteReservation.add_reservation'
    template_name = 'SiteReservation/reservation_add.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:index')
    form_post_url = reverse_lazy('reservation:ordinary:add')

    def form_valid(self, form):
        site = form.cleaned_data['site']
        activity_time_from = form.cleaned_data['activity_time_from']
        activity_time_to = form.cleaned_data['activity_time_to']

        conflict = is_conflict(activity_time_from, activity_time_to, site)
        if conflict:
            context = self.get_context_data()
            context['form'] = form
            html = render_to_string(
                self.template_name, request=self.request,
                context=context)
            return JsonResponse({'status': 2,
                                 'reason': _('Conflict with existing '
                                             'reservation'),
                                 'html': html})

        form.instance.user = self.request.user
        self.object = form.save()
        assign_perms('reservation', self.request.user, self.object,
                     perms=['update', 'view'])
        assign_perms('reservation', self.object.workshop.group, self.object,
                     perms=['update', 'view'])
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def get_object(self, queryset=None):
        return None

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.success_url
        return super(ReservationAdd, self).get_context_data(**kwargs)


class ReservationUpdate(ReservationBase, PermissionRequiredMixin, UpdateView):
    """
    A view for updating an exist reservation. Should check status before
    change, reject change if not match specified status.
    """
    raise_exception = True
    permission_required = 'update_reservation'
    template_name = 'SiteReservation/reservation_update.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:index')
    form_post_url = 'reservation:ordinary:update'

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.success_url
        return super(ReservationUpdate, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_ajax = request.is_ajax()
        allowed_status = self.object.status in RESERVATION_STATUS_CAN_EDIT
        if not is_ajax or not allowed_status:
            return HttpResponseForbidden()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in RESERVATION_STATUS_CAN_EDIT
        if not allowed_status:
            return HttpResponseForbidden()
        return super(ReservationUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        site = form.cleaned_data['site']
        activity_time_from = form.cleaned_data['activity_time_from']
        activity_time_to = form.cleaned_data['activity_time_to']

        conflict = is_conflict(activity_time_from, activity_time_to, site)
        if conflict:
            context = self.get_context_data()
            context['form'] = form
            html = render_to_string(
                self.template_name, request=self.request,
                context=context)
            return JsonResponse({'status': 2,
                                 'reason': _('Conflict with existing '
                                             'reservation'),
                                 'html': html})
        self.object.status = RESERVATION_SUBMITTED
        self.object = form.save()
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})
