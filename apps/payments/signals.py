from django.dispatch import receiver
from django.db.models.signals import post_save


#local imports
from .models import Group


@receiver(post_save, sender=Group)
def create_group_object_with_key(sender, instance, created, **kwargs):
    if created and instance.key==None:
        instance.key = instance.name
        instance.save()
    return instance


