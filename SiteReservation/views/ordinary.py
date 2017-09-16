#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:03
# Last modified: 2017-09-16 10:43
# Filename: ordinary.py
# Description:
from datetime import datetime, timedelta, timezone

from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.views.generic import DetailView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect


from authentication import USER_IDENTITY_STUDENT, USER_IDENTITY_TEACHER
from authentication import USER_IDENTITY_ADMIN
from SiteReservation.models import Reservation
from SiteReservation.forms import DateForm
from const.models import Site


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class ReservationBase(LoginRequiredMixin):
    """
    A base view for all reservation actions. SHOULD NOT DIRECTLY USE THIS.
    """

    model = Reservation


class ReservationRedirect(ReservationBase, RedirectView):
    """
    A view for redirect admin users and ordinary users.
    """

    def get(self, request, *args, **kwargs):
        identity = request.user.user_info.identity
        if identity == USER_IDENTITY_STUDENT:
            return redirect(reverse('reservation:status'))
        elif identity == USER_IDENTITY_TEACHER:
            pass
        elif identity == USER_IDENTITY_ADMIN:
            return redirect(reverse('reservation:admin:list'))
        else:
            raise Http404()


class ReservationStatus(ReservationBase, FormView):
    template_name = 'SiteReservation/reservation_status.html'
    status_table_name = 'SiteReservation/status_table.html'
    form_class = DateForm

    def get_context_data(self, **kwargs):
        kwargs['sites'] = Site.objects.all().order_by('desc')
        return super(ReservationStatus, self).get_context_data(**kwargs)

    def form_valid(self, form):
        uid = self.request.POST.get('site_uid', None)
        date = form.cleaned_data['date']
        start_dt = datetime.combine(date, datetime.min.time(), timezone.utc)
        end_dt = start_dt + timedelta(days=1)
        if not uid:
            raise Http404()
        site = get_object_or_404(Site, uid=uid)
        reservations = Reservation.objects.filter(site=site)
        reservations = reservations.filter(
            activity_time_from__range=(start_dt, end_dt))  # day range
        available_status = [True for _ in range(14)]  # 0 -> 08:00 ~ 09:00
        for r in reservations:
            for hour in range(r.activity_time_from, r.activity_time_to):
                available_status[hour] = False
        status_table = render_to_string(
            self.status_table_name, request=self.request,
            context={'available_status': available_status,
                     'date': date,
                     'site': site})
        return JsonResponse({'status': 0, 'html': status_table})

    def form_invalid(self, form):
        return JsonResponse({'status': 1})


class ReservationList(ReservationBase, ListView):
    """
    A view for displaying user-related reservations list. GET only.
    """

    pass


class ReservationDetail(ReservationBase, DetailView):
    """
    A view for displaying specified reservation. GET only.
    """

    pass


class ReservationAdd(ReservationBase, CreateView):
    """
    A view for creating a new reservation.
    """

    pass


class ReservationUpdate(ReservationBase, UpdateView):
    """
    A view for updating an exist reservation. Should check status before
    change, reject change if not match specified status.
    """

    pass
