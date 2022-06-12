from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.db.models import Q
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

#local imports
from .models import Group, GroupPayments, MonthlyPayments


@receiver(post_save, sender=Group)
def create_group_object_with_key(sender, instance, created, **kwargs):
    if created and instance.key==None:
        instance.key = instance.name.replace(' ', '_')
        instance.save()
    return instance


@receiver(post_save, sender=GroupPayments)
def update_group_paid_amount(sender, instance,  created, **kwargs):
    group = instance.group
    if not instance.payment_amount:
        instance.payment_amount = group.cost
        instance.save()

    if created:
        mpayment, created = MonthlyPayments.objects.get_or_create(
            month=group.month,
            year=group.year,
            created_by=group.created_by
        )
        mpayment.pupils += 1
        mpayment.save() 
    payments = GroupPayments.objects.filter(group=group)
    
    paid = payments.filter(Q(paid_admin=True)|Q(paid_director=True))
    must_paid = payments.filter(paid_admin=False, paid_director=False)
    
    group.paid = sum([obj.payment_amount for obj in paid])
    group.must_paid = sum([obj.payment_amount for obj in must_paid if obj.payment_amount])
    group.modified_by = instance.modified_by
    group.save()
    return instance

@receiver(pre_delete, sender=GroupPayments)
def update_group_paid_amount_del(sender, instance, **kwargs):
    if instance.paid_admin or instance.paid_director:
        raise ValidationError('To`lov allaqachon amalga oshirilgan')
    group = instance.group
    if group is None:
        return 
    if instance.paid_admin or instance.paid_director:
        group.paid = group.paid - instance.payment_amount
    else:
        group.must_paid = group.must_paid - instance.payment_amount
    group.save()
    
    mpayment, created = MonthlyPayments.objects.get_or_create(
            month=group.month,
            year=group.year,
            created_by=group.created_by
        )
    mpayment.pupils -= 1
    mpayment.save()
    return instance

@receiver(post_save, sender=Group)
def updating_monthlypayments_after_group_changing(sender, instance, created, **kwargs):
    mpayment, created = MonthlyPayments.objects.get_or_create(
        month=instance.month,
        year=instance.year,
        created_by=instance.created_by
    )
    groups = Group.objects.filter(
        month=instance.month,
        year=instance.year,
        created_by=instance.created_by
    )
    mpayment.paid = sum([group.paid for group in groups if group.paid])
    mpayment.must_paid = sum([group.must_paid for group in groups if group.must_paid])
    mpayment.modified_by = instance.modified_by
    mpayment.save()
    
    return instance

    