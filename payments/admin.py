from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('resident', 'apartment', 'concept', 'amount', 'status', 'period', 'payment_date', 'registered_by')
    list_filter = ('status', 'payment_method', 'concept', 'period')
    search_fields = ('resident__full_name', 'resident__cedula', 'apartment__number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-period',)