from django.db import models


class BankAccount(models.Model):
    CURRENCIES = (
        ('RUR', 'Russian Rouble'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro')
    )
    label = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    currency = models.CharField(max_length=3,
                                choices=CURRENCIES,
                                default='RUR')
    balance = models.DecimalField(max_digits=10,
                                  decimal_places=2,
                                  default=0)

