from django.db import models
from django.contrib.auth.models import User
from django.db.transaction import atomic
from autoslug import AutoSlugField

TR_ADD = 1
TR_WITHDRAW = 2
TR_MOVE = 3

TR_TYPES = (
    (TR_ADD, 'add'),
    (TR_WITHDRAW, 'withdraw'),
    (TR_MOVE, 'move'),
)
CURRENCIES = (
        ('RUB', 'Russian Rouble'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro')
    )
TR_TAG_CHOICES = (
    (0, ''),
    (1, 'Equity'),
    (2, 'Asset'),
    (3, 'Liability'),
    (4, 'Income'),
    (5, 'Expense'),
)


class BankAccount(models.Model):
    label = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='label')
    creation_date = models.DateField(auto_now_add=True, editable=False)
    currency = models.CharField(max_length=3,
                                choices=CURRENCIES,
                                default='RUR')

    balance = models.DecimalField(max_digits=12,
                                  decimal_places=2,
                                  default=0)
    owner = models.ForeignKey(User)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.owner.username + " " + self.label + " " + str(self.balance) + " " + self.currency

    @atomic
    def add_money(self, amount, tag, description):
        self.balance += amount
        transaction = self._create_transaction(TR_ADD, amount, tag, description)
        self.save()
        transaction.save()

    @atomic
    def withdraw_money(self, amount, tag, description):
        if (self.balance - amount) < 0:
            raise Exception("Withdraw amount couldn't be more than account balance")
        self.balance -= amount
        transaction = self._create_transaction(TR_WITHDRAW, amount, tag, description)
        self.save()
        transaction.save()

    @atomic
    def move_money(self, to_account, amount, tag, description):
        if (self.balance - amount) < 0:
            raise Exception("Withdraw amount couldn't be more than account balance")
        if self.currency != to_account.currency:
            raise Exception("Different currencies")
        if self.owner == to_account.owner and self.slug == to_account.slug:
            raise Exception("Sender and recipient accounts are the same")
        self.balance -= amount
        to_account.balance += amount
        transaction = self._create_transaction(TR_MOVE, amount, tag, description, to_account)
        self.save()
        to_account.save()
        transaction.save()

    def _create_transaction(self, tr_type, amount, tag, description, recipient=None):
        if amount < 0:
            raise Exception("Invalid amount")
        recipient_balance = None
        if recipient:
            recipient_balance = recipient.balance
        return Transaction(tr_from=self, tr_type=tr_type,
                           tr_to=recipient,
                           tr_amount=amount,
                           tr_tag=tag,
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
    tr_type = models.SmallIntegerField(choices=TR_TYPES)
    tr_tag = models.SmallIntegerField(choices=TR_TAG_CHOICES)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    recipient_balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3,
                                choices=CURRENCIES,
                                default='RUR')