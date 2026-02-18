from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import LoanProduct, LoanApplication
from .serializers import LoanProductSerializer, LoanApplicationSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



class LoanProductListView(generics.ListAPIView):
    queryset = LoanProduct.objects.all()
    serializer_class = LoanProductSerializer


class LoanApplicationCreateView(generics.CreateAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class LoanApplicationListView(generics.ListAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'manager':
            return LoanApplication.objects.all()

        return LoanApplication.objects.filter(customer=user)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'


class LoanStatusUpdateView(generics.UpdateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated, IsManager]

@login_required
def apply_loan_view(request):
    products = LoanProduct.objects.all()

    if request.method == 'POST':
        product_id = request.POST['loan_product']
        amount = request.POST['amount']
        duration = request.POST['duration']
        income = request.POST['income']

        LoanApplication.objects.create(
            customer=request.user,
            loan_product_id=product_id,
            amount=amount,
            duration_months=duration,
            monthly_income=income
        )

        return redirect('/my-loans/')

    return render(request, 'apply_loan.html', {'products': products})


@login_required
def my_loans_view(request):
    if request.user.role == 'manager':
        loans = LoanApplication.objects.all()
    else:
        loans = LoanApplication.objects.filter(customer=request.user)

    return render(request, 'loan_list.html', {'loans': loans})
