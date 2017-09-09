#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 08:47
# Last modified: 2017-09-09 09:37
# Filename: __init__.py
# Description:
from .ordinary import ReservationList, ReservationAdd, ReservationUpdate
from .ordinary import ReservationRedirect, ReservationDetail
from .admin import AdminReservationList, AdminReservationUpdate
from .admin import AdminReservationDetail


__all__ = [
    'ReservationRedirect', 'ReservationDetail', 'AdminReservationDetail',
    'ReservationList', 'ReservationAdd', 'ReservationUpdate',
    'AdminReservationList', 'AdminReservationUpdate',
]
