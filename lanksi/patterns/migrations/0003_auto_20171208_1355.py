# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 10:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patterns', '0002_transactiontemplate_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactiontemplate',
            name='transaction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Transaction'),
        ),
    ]