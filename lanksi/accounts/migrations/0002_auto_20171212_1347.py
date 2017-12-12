# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient_currency',
            field=models.CharField(blank=True, choices=[('RUB', 'Russian Rouble'), ('USD', 'US Dollar'), ('EUR', 'Euro')], max_length=3, null=True, verbose_name='Recipient currency'),
        ),
    ]
