from django.urls import path
from .views import (
    LoanProductListView,
    LoanApplicationCreateView,
    LoanApplicationListView,
    LoanStatusUpdateView,
)


urlpatterns = [
    path('products/', LoanProductListView.as_view(), name='loan-products'),
    path('apply/', LoanApplicationCreateView.as_view(), name='loan-apply'),
    path('my-loans/', LoanApplicationListView.as_view(), name='my-loans'),
    path('update/<int:pk>/', LoanStatusUpdateView.as_view(), name='loan-update'),
]
