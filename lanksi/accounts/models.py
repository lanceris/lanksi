from django.db import models
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.conf import settings
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from categories.models import Category




class BankAccount(models.Model):
    label = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='label', unique=True)
    creation_date = models.DateField(auto_now_add=True, editable=False)
    currency = models.CharField(max_length=3,
                                choices=settings.CURRENCIES,
                                default='RUB')

    balance = models.DecimalField(max_digits=12,
                                  decimal_places=2,
                                  default=0)
    owner = models.ForeignKey(User)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.label

    @atomic
    def add_money(self, amount, tag, category, description):
        self.balance += amount
        transaction = self._create_transaction(settings.TR_ADD, amount, tag, category, description)
        self.save()
        transaction.save()

    @atomic
    def withdraw_money(self, amount, tag, category, description):
        if (self.balance - amount) < 0:
            raise Exception("Withdraw amount couldn't be more than account balance")
        self.balance -= amount
        transaction = self._create_transaction(settings.TR_WITHDRAW, amount,  tag, category, description)
        self.save()
        transaction.save()

    @atomic
    def move_money(self, to_account, amount, category, tag, description):
        if (self.balance - amount) < 0:
            raise Exception("Withdraw amount couldn't be more than account balance")
        if self.currency != to_account.currency:
            raise Exception("Different currencies")
        if self.owner == to_account.owner and self.slug == to_account.slug:
            raise Exception("Sender and recipient accounts are the same")
        self.balance -= amount
        to_account.balance += amount
        transaction = self._create_transaction(settings.TR_MOVE, amount, tag, category, description, to_account)
        self.save()
        to_account.save()
        transaction.save()

    def _create_transaction(self, tr_type, amount, tag, category, description, recipient=None):
        if amount < 0:
            raise Exception("Invalid amount")
        recipient_balance = None
        if recipient:
            recipient_balance = recipient.balance
        return Transaction(tr_from=self, tr_type=tr_type,
                           tr_to=recipient,
                           tr_amount=amount,
                           tr_tag=tag,
                           category=category,
                           balance=self.balance,
                           recipient_balance=recipient_balance,
                           comment=description)


class Transaction(models.Model):
    tr_from = models.ForeignKey(BankAccount)
    tr_to = models.ForeignKey(BankAccount, blank=True, null=True, related_name='tr_to')
    comment = models.TextField(blank=True, null=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    tr_amount = models.DecimalField(max_digits=12,
                                    decimal_places=2,
                                    default=0)
    tr_type = models.SmallIntegerField(choices=settings.TR_TYPES)
    tr_tag = TaggableManager()
    category = models.ForeignKey(Category, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    recipient_balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3,
                                choices=settings.CURRENCIES,
                                default='RUB')
