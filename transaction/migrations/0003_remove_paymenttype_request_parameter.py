# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 05:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_paymenttype_function_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenttype',
            name='request_parameter',
        ),
    ]
