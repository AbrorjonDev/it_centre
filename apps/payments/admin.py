from django.contrib import admin

#local imports
from .models import Group, GroupPayments



admin.site.register(Group)
admin.site.register(GroupPayments)
