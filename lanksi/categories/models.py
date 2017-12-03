from django.db import models
from lanksi.accounts.models import TR_TYPES

class Category(models.Model):
    cat_type = models.SmallIntegerField(choices=TR_TYPES)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)