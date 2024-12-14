from django.contrib import admin
from .models import *

admin.site.register([User, Student, Faculty, StudentGroup, Specialty])