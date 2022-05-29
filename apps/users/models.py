from django.db import models
from django.contrib.auth.models import AbstractUser

#local imports
from base_model.models import BaseModel


class User(AbstractUser, BaseModel):
    is_admin = models.BooleanField(default=True)
    is_director = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username