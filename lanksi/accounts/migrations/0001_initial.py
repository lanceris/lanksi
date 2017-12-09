# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 17:09
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='label', unique=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('currency', models.CharField(choices=[('RUB', 'Russian Rouble'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='RUB', max_length=3)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('description', models.TextField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(max_length=3)),
                ('other_currency', models.CharField(max_length=3)),
                ('value', models.DecimalField(decimal_places=3, max_digits=8)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tr_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('tr_type', models.SmallIntegerField(choices=[(1, 'Add'), (2, 'Withdraw'), (3, 'Move'), (4, 'Exchange')])),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12)),
                ('recipient_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('currency', models.CharField(choices=[('RUB', 'Russian Rouble'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='RUB', max_length=3)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
                ('tr_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BankAccount')),
                ('tr_tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('tr_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tr_to', to='accounts.BankAccount')),
            ],
        ),
    ]
