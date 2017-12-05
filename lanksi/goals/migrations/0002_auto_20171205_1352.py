# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 10:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='money_left',
        ),
        migrations.AddField(
            model_name='goal',
            name='money_saved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=26),
        ),
    ]
