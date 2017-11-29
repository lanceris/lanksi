from django.contrib import admin

from .models import BankAccount

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['label', 'balance', 'currency', 'creation_date']
    list_display_links = ['label']
    ordering = ['label']
    search_fields = ['label']