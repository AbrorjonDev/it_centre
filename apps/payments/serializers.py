from rest_framework import serializers
from django.contrib.auth import get_user_model


#local imports
from .models import Group, GroupPayments
from users.serializers import UserSerializer


class GroupPaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupPayments
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    payments = GroupPaymentsSerializer(required=False, read_only=True)
    created_by = UserSerializer(many=False, required=False)
    modified_by = UserSerializer(many=False, required=False)

    class Meta:
        model = Group
        fields = ("id", "name", "cost", "key", "lessons_count", "payments", "created_by", "modified_by")