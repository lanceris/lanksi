# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 12:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_type', models.SmallIntegerField(choices=[(1, 'add'), (2, 'withdraw'), (3, 'move'), (4, 'exchange')])),
                ('name', models.CharField(max_length=255)),
                ('money', models.DecimalField(decimal_places=2, max_digits=26)),
                ('currency', models.CharField(choices=[('RUB', 'Russian Rouble'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='RUB', max_length=3)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]