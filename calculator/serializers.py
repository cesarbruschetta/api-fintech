from rest_framework import serializers
from decimal import Decimal
from datetime import datetime, timezone

from .models import Loan, Payment, Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

    def to_representation(self, obj):
        return {"client_id": str(obj.id)}


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

    def to_representation(self, obj):
        return {"id": str(obj.id), "installment": round(float(obj.instalment), 2)}

    def validate_client(self, client):
        if client.is_indebt:
            raise serializers.ValidationError("Denied loan request")
        return client

    def validate_client(self, client):
        if client.is_indebted:
            raise serializers.ValidationError("Denied loan request")
        return client


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def to_representation(self, obj):
        return {}


class BalanceSerializer(serializers.Serializer):
    date = serializers.DateTimeField(
        "Date base to balance",
        required=False,
        allow_null=True,
        default=datetime.now().astimezone(tz=timezone.utc),
    )
    loan_id = serializers.CharField(max_length=None)

    def to_representation(self, obj):
        if not obj["date"]:
            obj["date"] = datetime.now().astimezone(tz=timezone.utc)
        return {"balance": self.loan.get_balance(obj["date"])}
    
    def validate(self, data):
        self.loan = Loan.objects.get(pk=data["loan_id"])
        if data["date"]:
            if data["date"] < self.loan.date_initial:
                raise serializers.ValidationError("The date should be greater than the initial date loan")
        return data
