from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from categories.models import Category


class Goal(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    money_total = models.DecimalField(max_digits=26,
                                      decimal_places=2)
    money_saved = models.DecimalField(max_digits=26, decimal_places=2, default=0)
    currency = models.CharField(max_length=3,
                                choices=settings.CURRENCIES,
                                default='RUB')
    description = models.TextField(blank=True, null=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_money_left(self):
        return self.money_total - self.money_saved

    def add_money(self, amount, acc_from):
        if amount < 0:
            raise Exception('Amount should be > 0')
        elif amount + self.money_saved >= self.money_total:
            raise Exception('Too much money to add')
        elif acc_from.balance - amount < 0:
            raise Exception('Not enough money')
        else:
            self.money_saved += amount
            acc_from.withdraw_money(amount, '', Category.objects.get(name='To goal'), '')
            self.save()


