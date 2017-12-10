from django.db import models
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.conf import settings
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from categories.models import Category
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class BankAccount(models.Model):
    label = models.CharField(max_length=255,
                             verbose_name=_('Name'))
    slug = AutoSlugField(populate_from='label',
                         unique=True,
                         verbose_name=_('Slug'))
    creation_date = models.DateField(auto_now_add=True,
                                     editable=False,
                                     verbose_name=_('Created'))
    currency = models.CharField(max_length=3,
                                choices=settings.CURRENCIES,
                                default='RUB',
                                verbose_name=_('Currency'))

    balance = models.DecimalField(max_digits=12,
                                  decimal_places=2,
                                  default=0,
                                  verbose_name=_('Balance'))
    owner = models.ForeignKey(User,
                              verbose_name=_('Owner'))
    description = models.TextField(blank=True,
                                   verbose_name=_('Description'))

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('Bank Account')
        verbose_name_plural = _('Bank Accounts')

    @atomic
    def add_money(self, amount, tags, category, description):
        self.balance += amount
        transaction = self._create_transaction(settings.TR_ADD, amount, tags, category, description)
        self.save()
        transaction.save()

    @atomic
    def withdraw_money(self, amount, tags, category, description):
        if (self.balance - amount) < 0:
            raise Exception("Withdraw amount couldn't be more than account balance")
        self.balance -= amount
        transaction = self._create_transaction(settings.TR_WITHDRAW, amount,  tags, category, description)
        self.save()
        transaction.save()

    @atomic
    def move_money(self, to_account, amount, category, tags, description):
        if (self.balance - amount) < 0:
            raise Exception("Withdraw amount couldn't be more than account balance")
        if self.currency != to_account.currency:
            raise Exception("Different currencies")
        if self.owner == to_account.owner and self.slug == to_account.slug:
            raise Exception("Sender and recipient accounts are the same")
        self.balance -= amount
        to_account.balance += amount
        transaction = self._create_transaction(settings.TR_MOVE, amount, tags, category, description, to_account)
        self.save()
        to_account.save()
        transaction.save()

    @atomic
    def exchange_money(self,
                       to_account,
                       amount,
                       currency_from,
                       currency_to,
                       tags,
                       category,
                       description):
        exchange_rate = ExchangeRate.objects.get(base_currency=currency_to,
                                                 other_currency=currency_from).value
        self.balance -= amount
        to_account.balance += amount/exchange_rate
        transaction = self._create_transaction(settings.TR_EXCHANGE, amount, tags, category, description)
        self.save()
        transaction.save()
        to_account.save()

    def _create_transaction(self, tr_type, amount, tags, category, description, recipient=None):
        if amount < 0:
            raise Exception("Invalid amount")
        recipient_balance = None
        if recipient:
            recipient_balance = recipient.balance
        return Transaction(tr_from=self, tr_type=tr_type,
                           tr_to=recipient,
                           tr_amount=amount,
                           tr_tags=tags,
                           category=category,
                           balance=self.balance,
                           recipient_balance=recipient_balance,
                           comment=description)


class Transaction(models.Model):
    tr_from = models.ForeignKey(BankAccount, verbose_name=_('From'))
    tr_to = models.ForeignKey(BankAccount,
                              blank=True,
                              null=True,
                              related_name='tr_to',
                              verbose_name=_('To'))
    comment = models.TextField(blank=True,
                               null=True,
                               max_length=255,
                               verbose_name=_('Comment'))
    created = models.DateTimeField(auto_now_add=True,
                                   editable=False,
                                   verbose_name=_('Created'))
    tr_amount = models.DecimalField(max_digits=12,
                                    decimal_places=2,
                                    default=0,
                                    verbose_name=_('Amount'))
    tr_type = models.SmallIntegerField(choices=settings.TR_TYPES,
                                       verbose_name=_('Type'))
    tr_tags = TaggableManager(blank=True, verbose_name=_('Tags'))
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name=_('Category'))
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Balance'))
    recipient_balance = models.DecimalField(max_digits=12,
                                            decimal_places=2,
                                            blank=True,
                                            null=True,
                                            verbose_name=_('Recipient balance'))
    currency = models.CharField(max_length=3,
                                choices=settings.CURRENCIES,
                                default='RUB',
                                verbose_name=_('Currency'))

    def __str__(self):
        try:
            msg = self.tr_from.label + " -> " + self.tr_to.label + " at " + self.created.strftime('%d/%m/%Y')
        except:
            msg = self.tr_from.label + " -> " + "None" + " at " + self.created.strftime('%d/%m/%Y %H:%M:%S')
        return msg

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')


class ExchangeRate(models.Model):
    base_currency = models.CharField(max_length=3, verbose_name=_('Base currency'))
    other_currency = models.CharField(max_length=3, verbose_name=_('Other currency'))
    value = models.DecimalField(max_digits=8, decimal_places=3, verbose_name=_('Value'))
    date = models.DateField(editable=True, default=now, verbose_name=_('Date'))

    def __str__(self):
        return self.base_currency+"/"+self.other_currency

    class Meta:
        verbose_name = _('Exchange Rate')
        verbose_name_plural = _('Exchange Rates')
