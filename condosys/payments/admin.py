from django.contrib import admin
from .models import Payment, ChargeType


@admin.register(ChargeType)
class ChargeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartment', 'charge_type', 'amount', 'status', 'due_date', 'is_overdue')
    list_filter = ('status', 'payment_method', 'invoice_date', 'due_date')
    search_fields = ('apartment__number', 'reference_number')
    readonly_fields = ('created_at', 'updated_at', 'is_overdue')
    ordering = ('-invoice_date',)

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.short_description = 'Is Overdue'
    is_overdue.boolean = True

