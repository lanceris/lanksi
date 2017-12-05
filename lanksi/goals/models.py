from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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

    def add_money(self, amount):
        if amount < 0:
            raise Exception('Amount should be > 0')
        elif amount + self.money_saved >= self.money_total:
            raise Exception('')
        else:
            self.money_saved += amount

