from django.db import models
from django.contrib.auth.models import User
from accounts.models import Transaction


class TransactionTemplate(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    transaction = models.ForeignKey(Transaction)
    description = models.TextField(blank=True, null=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)