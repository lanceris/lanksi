# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 22:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Transaction', verbose_name='Transaction')),
            ],
            options={
                'verbose_name': 'Transaction Template',
                'verbose_name_plural': 'Transaction Templates',
            },
        ),
    ]
