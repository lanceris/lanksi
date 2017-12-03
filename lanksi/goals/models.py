from django.db import models
from django.contrib.auth.models import User
from lanksi.accounts.models import TR_TYPES, CURRENCIES


class Goal(models.Model):
    goal_type = models.SmallIntegerField(choices=TR_TYPES)
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    money = models.DecimalField(max_digits=26,
                                decimal_places=2)
    currency = models.CharField(max_length=3,
                                choices=CURRENCIES,
                                default='RUB')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


