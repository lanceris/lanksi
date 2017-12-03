from django.contrib import admin

from .models import BankAccount, Transaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['owner', 'label', 'slug', 'balance', 'currency', 'creation_date']
    list_display_links = ['label']
    list_filter = ('owner', 'label', 'balance', 'creation_date')
    ordering = ['label']
    search_fields = ['label']


admin.site.register(Transaction)
