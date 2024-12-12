from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    first_name = models.CharField(max_length=50, verbose_name=_("first name"))
    last_name = models.CharField(max_length=50, verbose_name=_("last name"))
    patronymic = models.CharField(max_length=50, verbose_name=_("patronymic"))
    username = models.CharField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"

class PupilClass(BaseModel):
    TYPE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    number = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(11)],
        verbose_name=_("number")
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, verbose_name=_("type"))

    def __str__(self):
        return f"{self.number}-{self.type}"
    
class Pupil(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    pupil_class = models.ForeignKey(PupilClass, on_delete=models.CASCADE, verbose_name=_("pupil class"))

    def __str__(self):
        return self.user.get_full_name