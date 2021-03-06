from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

#local imports
from .models import Group, GroupPayments, MonthlyPayments
from apps.users.serializers import UserSerializer


class GroupPaymentsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(required=False, many=False)
    modified_by = UserSerializer(required=False, many=False)
    deadline = serializers.BooleanField(default=False, required=False)
    payment = serializers.FloatField(required=False)
    
    class Meta:
        model = GroupPayments
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
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
            "paid",
            "must_paid",
            "month",
            "year",
            "created_by", 
            "modified_by",
            "date_created",
            "date_modified",
            )

    def create(self, attrs):
        user = self.context["request"].user
        if attrs.get('month', None) is None:
            attrs['month'] = timezone.now().month

        if attrs.get('year', None) is None:            
            attrs['year'] = timezone.now().year

        group = Group.objects.create(**attrs, created_by=user)
        return group


class GroupDetailSerializer(serializers.ModelSerializer):
    payments = GroupPaymentsSerializer(required=False, read_only=True, many=True)
    created_by = UserSerializer(many=False, required=False, read_only=True)
    modified_by = UserSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = Group
        fields = "__all__"
    def update(self, instance, attrs):
        instance.name = attrs.get("name", instance.name)
        instance.cost = attrs.get("cost", instance.cost)
        instance.month = attrs.get("month", instance.month)
        instance.year = attrs.get("year", instance.year)
        instance.key = attrs.get("key", instance.key)
        instance.lessons_count = attrs.get("lessons_count", instance.lessons_count)
        instance.modified_by = self.context["request"].user
        instance.save()
        return instance


class GroupPaymentsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPayments
        fields = (
            "id",
            "full_name",
            "payment_amount",
            "paid_admin",
            "paid_director",
            "payment_date",
            "lessons_count",
            "group"
            )
    def validate(self, attrs):
        attrs = super().validate(attrs)
        instance = getattr(self, 'instance', None)
        if instance is not None and instance.group is None and "group" not in attrs.keys():
            raise ValidationError('Bad Request! --- group tanlanmagan.')
        if ((attrs["group"].created_by == self.context["request"].user) or
            (attrs["group"].created_by == self.context["request"].user.created_by) or
            (self.instance and self.instance.group is not None and self.instance.group.created_by==(self.context['request'].user or self.context['request'].user.created_by))):
            return attrs
        raise ValidationError('Forbidden!--- Bu guruh sizga tegishli emas!')

    def create(self, attrs):
        try:
            payment = GroupPayments.objects.get(**attrs)
            if payment.date_created.month == timezone.now().month:
                return payment
        except:
            pass
        #Todo: admin cannot add paid_director status, and another point.
        if "paid_admin" in attrs.keys() and not self.context["request"].user.is_admin:
            attrs.pop("paid_admin")
        if "paid_director" in attrs.keys() and not self.context["request"].user.is_director:
            attrs.pop("paid_director")
        
        student = GroupPayments.objects.create(**attrs, created_by=self.context["request"].user)
        student.save()
        return student

    def update(self, instance, attrs):
        instance.full_name = attrs.get("full_name", instance.full_name)
        instance.payment_amount = attrs.get("payment_amount", instance.payment_amount)
        if self.context['request'].user.is_admin:
            instance.paid_admin = attrs.get("paid_admin", instance.paid_admin)
        elif self.context['request'].user.is_director:
            instance.paid_director = attrs.get("paid_director", instance.paid_director)
        instance.payment_date = attrs.get("payment_date", instance.payment_date)
        instance.lessons_count = attrs.get("lessons_count", instance.lessons_count)
        instance.group = attrs.get("group", instance.group)
        instance.modified_by = self.context["request"].user
        instance.date_modified = timezone.now()
        instance.save()
        return instance


class MonthlyPaymentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = MonthlyPayments
        fields = (
            "id", "paid", "must_paid", "pupils", "created_by"
        )
