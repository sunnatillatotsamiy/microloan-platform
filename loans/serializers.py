from rest_framework import serializers
from .models import LoanProduct, LoanApplication, RiskTag


class LoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProduct
        fields = '__all__'


class RiskTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskTag
        fields = '__all__'


class LoanApplicationSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = LoanApplication
        fields = '__all__'
