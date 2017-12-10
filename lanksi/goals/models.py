from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from categories.models import Category
from django.utils.translation import ugettext_lazy as _


class Goal(models.Model):
    owner = models.ForeignKey(User, verbose_name=_('Owner'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    money_total = models.DecimalField(max_digits=26,
                                      decimal_places=2,
                                      verbose_name=_('Total'))
    money_saved = models.DecimalField(max_digits=26,
                                      decimal_places=2,
                                      default=0,
                                      verbose_name=_('Saved'))
    currency = models.CharField(max_length=3,
                                choices=settings.CURRENCIES,
                                default='RUB',
                                verbose_name=_('Currency'))
    description = models.TextField(blank=True,
                                   null=True,
                                   max_length=255,
                                   verbose_name=_('Description'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')

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
            if Category.objects.filter(name='To goal').exists():
                self.money_saved += amount
                acc_from.withdraw_money(amount, '', Category.objects.get(name='To goal'), '')
                self.save()
            else:
                new_cat = Category.objects.create(cat_type=2,
                                                  name='To goal',
                                                  owner=self.owner)
                new_cat.save()
                self.money_saved += amount
                acc_from.withdraw_money(amount, '', Category.objects.get(name='To goal'), '')
                self.save()

