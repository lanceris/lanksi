# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 11:28
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankaccount',
            options={'verbose_name': 'Bank Account', 'verbose_name_plural': 'Bank Accounts'},
        ),
        migrations.AlterModelOptions(
            name='exchangerate',
            options={'verbose_name': 'Exchange Rate', 'verbose_name_plural': 'Exchange Rates'},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'verbose_name': 'Transaction', 'verbose_name_plural': 'Transactions'},
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='currency',
            field=models.CharField(choices=[('RUB', 'Russian Rouble'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='RUB', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='label',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='label', unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='base_currency',
            field=models.CharField(max_length=3, verbose_name='Base currency'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='other_currency',
            field=models.CharField(max_length=3, verbose_name='Other currency'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='value',
            field=models.DecimalField(decimal_places=3, max_digits=8, verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.CharField(choices=[('RUB', 'Russian Rouble'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='RUB', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recipient_balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Recipient balance'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tr_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tr_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BankAccount', verbose_name='From'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tr_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tr_to', to='accounts.BankAccount', verbose_name='To'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tr_type',
            field=models.SmallIntegerField(choices=[(1, 'Add'), (2, 'Withdraw'), (3, 'Move'), (4, 'Exchange')], verbose_name='Type'),
        ),
    ]