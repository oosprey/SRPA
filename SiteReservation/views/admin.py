#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:03
# Last modified: 2017-09-09 10:08
# Filename: admin.py
# Description:
from django.contrib.auth.mixins import LoginRequiredMixin

from .ordinary import ReservationList, ReservationUpdate, ReservationDetail


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class AdminReservationBase(LoginRequiredMixin):
    """
    A base view for all admin reservation actions. SHOULD NOT DIRECTLY USE
    THIS. Check admin auth first.
    """

    pass


class AdminReservationList(AdminReservationBase, ReservationList):
    """
    A view for displaying reservations list for admin. GET only.
    """

    pass


class AdminReservationDetail(AdminReservationBase, ReservationDetail):
    """
    A view for displaying specified reservation for admin. GET only.
    """

    pass


class AdminReservationUpdate(AdminReservationBase, ReservationUpdate):
    """
    A view for admin to update an exist reservation.
    Should check status before change, reject change if not match
    specified status.
    """

    pass
