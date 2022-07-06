from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()


class BaseModel(models.Model):
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="+")
    modified_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="+")
    date_created = models.DateTimeField(null=True, auto_now_add=True)
    date_modified = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        abstract = True