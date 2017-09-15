#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:03
# Last modified: 2017-09-15 15:05
# Filename: ordinary.py
# Description:
from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.views.generic import DetailView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse


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

    pass


class ReservationStatus(ReservationBase, FormView):
    template_name = 'SiteReservation/reservation_status.html'
    form_class = DateForm

    def get_context_data(self, **kwargs):
        kwargs['sites'] = Site.objects.all().order_by('desc')
        return super(ReservationStatus, self).get_context_data(**kwargs)

    def form_valid(self, form):
        uid = self.request.POST.get('uid', None)
        if not uid:
            raise Http404()
        reservations = Reservation.objects.filter(site__uid=uid)
        return JsonResponse({'status': 0})


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
