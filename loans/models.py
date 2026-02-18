from django.db import models
from django.conf import settings


class LoanProduct(models.Model):
    name = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_min = models.IntegerField()
    duration_max = models.IntegerField()

    def __str__(self):
        return self.name


class RiskTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LoanApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loan_applications'
    )

    loan_product = models.ForeignKey(
        LoanProduct,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.IntegerField()
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    risk_tags = models.ManyToManyField(RiskTag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan #{self.id} - {self.customer.username}"


class ManagerReview(models.Model):
    loan = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='manager_reviews'
    )

    comment = models.TextField()
    decision_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.manager.username}"
