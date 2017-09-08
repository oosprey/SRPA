#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 16:23
# Last modified: 2017-09-08 16:25
# Filename: captcha_challenges.py
# Description:
import random

from captcha.conf import settings
from six import u


def random_num_challenge():
    chars, ret = u('0123456789'), u('')
    for i in range(settings.CAPTCHA_LENGTH):
        ret += random.choice(chars)
    return ret.upper(), ret
