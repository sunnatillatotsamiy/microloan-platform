from django.contrib import admin
from .models import LoanProduct, LoanApplication, RiskTag, ManagerReview


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest_rate', 'min_amount', 'max_amount')


@admin.register(RiskTag)
class RiskTagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'loan_product', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__username',)


@admin.register(ManagerReview)
class ManagerReviewAdmin(admin.ModelAdmin):
    list_display = ('loan', 'manager', 'decision_date')
