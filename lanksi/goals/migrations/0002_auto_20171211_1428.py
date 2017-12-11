# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 11:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goal',
            options={'verbose_name': 'Goal', 'verbose_name_plural': 'Goals'},
        ),
        migrations.AlterField(
            model_name='goal',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='currency',
            field=models.CharField(choices=[('RUB', 'Russian Rouble'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='RUB', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='money_saved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=26, verbose_name='Saved'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='money_total',
            field=models.DecimalField(decimal_places=2, max_digits=26, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
    ]
