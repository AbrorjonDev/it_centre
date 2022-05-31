from django.db import models
from django.contrib.auth import get_user_model


#local imports
from base_model.models import BaseModel

User = get_user_model()


class Group(BaseModel):
    name = models.CharField(max_length=100)
    cost = models.IntegerField(null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=True)
    lessons_count = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ("-id", )
    def __str__(self):
        return self.name
    
    @property
    def payments(self):
        return self.grouppayments_set.all()

class GroupPayments(BaseModel):
    full_name = models.CharField(max_length=140)
    payment_amount = models.IntegerField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    paid_admin = models.BooleanField(default=False)
    paid_director = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    lessons_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Student payment"
        verbose_name_plural = "Student payments"

    def __str__(self):
        return self.full_name