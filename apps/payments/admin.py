from django.contrib import admin

#local imports
from .models import Group, GroupPayments, MonthlyPayments



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "paid", "must_paid", "month", "year")
@admin.register(GroupPayments)
class GroupPaymentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "payment_amount", "group", "paid_admin", "paid_director")

@admin.register(MonthlyPayments)
class MonthlyPaymentAdmin(admin.ModelAdmin):
    list_display = ("created_by", "paid", "must_paid", "month", "year", "pupils")