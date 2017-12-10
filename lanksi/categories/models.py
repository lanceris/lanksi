from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    cat_type = models.SmallIntegerField(choices=settings.TR_TYPES, verbose_name=_('Type'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    slug = AutoSlugField(populate_from='name', unique=True, verbose_name=_('Slug'))
    owner = models.ForeignKey(User, verbose_name=_('Owner'))
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
