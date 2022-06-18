from django.db import models
from django.contrib.auth import get_user_model


#local imports
from base_model.models import BaseModel
 
User = get_user_model()

 
class Group(BaseModel):
    name = models.CharField(max_length=100)
    cost = models.IntegerField(null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=True)
    lessons_count = models.IntegerField(null=True, blank=True, default=0)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    paid = models.IntegerField(null=True, blank=True)
    must_paid = models.IntegerField(null=True, blank=True)

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

    @property
    def payment(self):
        payment_percentage = 0
        if self.group.lessons_count > 0:
            payment_percentage = self.lessons_count/self.group.lessons_count
        return self.payment_amount * payment_percentage 

class MonthlyPayments(BaseModel):
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    paid = models.IntegerField(null=True, blank=True)
    must_paid = models.IntegerField(null=True, blank=True)
    pupils = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self):
        return self.created_by.username if self.created_by else f'{self.id}'

class HistoryMessages(BaseModel):
    text = models.TextField(null=True, blank=True)
    payment = models.ForeignKey(GroupPayments, on_delete=models.SET_NULL, null=True)
    # created_by --> is admin created by director
    modified_by = None

    def __str__(self):
        return self.text
         