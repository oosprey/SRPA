# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-14 02:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20170914_1000'),
        ('const', '0002_auto_20170908_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='instructor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='authentication.TeacherInfo', verbose_name='指导教师'),
            preserve_default=False,
        ),
    ]
