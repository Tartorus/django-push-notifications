# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-17 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0007_uniquesetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gcmdevice',
            name='device_id',
            field=push_notifications.fields.HexDecimalField(blank=True, db_index=True, decimal_places=0, help_text='ANDROID_ID / TelephonyManager.getDeviceId() ', max_digits=100, null=True, verbose_name='Device ID'),
        ),
    ]
