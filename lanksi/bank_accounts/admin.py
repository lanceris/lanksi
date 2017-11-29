from django.contrib import admin

from .models import BankAccount

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['owner', 'label', 'balance', 'currency', 'creation_date']
    list_display_links = ['label']
    list_filter = ('owner', 'label', 'balance', 'creation_date')
    ordering = ['label']
    search_fields = ['label']
