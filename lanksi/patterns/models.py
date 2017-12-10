from django.db import models
from django.contrib.auth.models import User
from accounts.models import Transaction
from django.utils.translation import ugettext_lazy as _


class TransactionTemplate(models.Model):
    owner = models.ForeignKey(User, verbose_name=_('Owner'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    transaction = models.OneToOneField(Transaction, verbose_name=_('Transaction'))
    description = models.TextField(blank=True, null=True, max_length=255, verbose_name=_('Description'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Transaction Template')
        verbose_name_plural = _('Transaction Templates')