from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

#local imports
from .models import Group, GroupPayments
from apps.users.serializers import UserSerializer


class GroupPaymentsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(required=False, many=False)
    modified_by = UserSerializer(required=False, many=False)
    
    class Meta:
        model = GroupPayments
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    payments = GroupPaymentsSerializer(required=False, read_only=True, many=True)
    created_by = UserSerializer(many=False, required=False, read_only=True)
    modified_by = UserSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = Group
        fields = (
            "id", 
            "name", 
            "cost", 
            "key", 
            "lessons_count", 
            "payments", 
            "created_by", 
            "modified_by",
            "date_created",
            "date_modified"
            )

    def create(self, attrs):
        group = Group.objects.create(**attrs, created_by=self.context["request"].user)
        return group

    def update(self, instance, attrs):
        instance.name = attrs.get("name", instance.name)
        instance.cost = attrs.get("cost", instance.cost)
        instance.key = attrs.get("key", instance.key)
        instance.lessons_count = attrs.get("lessons_count", instance.lessons_count)
        instance.modified_by = self.context["request"].user
        instance.save()
        return instance


class GroupPaymentsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPayments
        fields = (
            "full_name",
            "payment_amount",
            "paid_admin",
            "paid_director",
            "payment_date",
            "lessons_count",
            "group"
            )
        
    def create(self, attrs):
        try:
            payment = GroupPayments.objects.get(**attrs)
            if payment.date_created.month == timezone.now().month:
                return payment
        except:
            pass
        student = GroupPayments.objects.create(**attrs, created_by=self.context["request"].user)
        student.save()
        return student

    def update(self, instance, attrs):
        instance.full_name = attrs.get("full_name", instance.full_name)
        instance.payment_amount = attrs.get("payment_amount", instance.payment_amount)
        instance.paid_admin = attrs.get("paid_admin", instance.paid_admin)
        instance.paid_director = attrs.get("paid_director", instance.paid_director)
        instance.payment_date = attrs.get("payment_date", instance.payment_date)
        instance.lessons_count = attrs.get("lessons_count", instance.lessons_count)
        instance.group = attrs.get("group", instance.group)
        instance.modified_by = self.context["request"].user
        instance.date_modified = timezone.now()
        instance.save()
        return instance