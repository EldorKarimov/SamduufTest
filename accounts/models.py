from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class Faculty(BaseModel):
    faculty_name = models.CharField(max_length=255, verbose_name=_('faculty'))

    def __str__(self):
        return self.faculty_name
    
    class Meta:
        verbose_name = _("faculty")
        verbose_name_plural = _("faculties")
    
class Specialty(BaseModel):
    specialty_name = models.CharField(max_length=150, verbose_name=_('name'))
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='faculty', verbose_name=_('faculty'))

    def __str__(self):
        return self.specialty_name
        
    
    class Meta:
        verbose_name = _("specialty")
        verbose_name_plural = _("specialties")

class StudentGroup(BaseModel):
    group_name = models.CharField(max_length=50, verbose_name=_("name"))
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='specialty', verbose_name=_("specialty"))

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = _("Student group")
        verbose_name_plural = _("Student groups")

class Student(BaseModel):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='student_group', verbose_name=_("student group"))
    user = models.OneToOneField("User", on_delete=models.CASCADE, verbose_name=_("user"))

    def __str__(self):
        return self.user.get_full_name

    @property
    def get_specialty(self):
        return self.group.specialty.name
    
    @property
    def get_faculty(self):
        return self.group.specialty.faculty.name

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

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
        

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"