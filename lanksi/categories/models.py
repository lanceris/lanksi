from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.contrib.auth.models import User


class Category(models.Model):
    cat_type = models.SmallIntegerField(choices=settings.TR_TYPES)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

