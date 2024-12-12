from django.db import models
from uuid import uuid4

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add = True)
    created = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True