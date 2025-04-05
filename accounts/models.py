from django.contrib.auth.models import AbstractUser
from django.db import models

class SarataniUser(AbstractUser):
    is_doctor               = models.BooleanField(default=True)
    CHOICES = (
                ("Male","Male"),
                ("Female","Female")
            )
    sex                     = models.CharField(choices=CHOICES, max_length=50, default="Male", blank=False, null=False)
    age                     = models.PositiveIntegerField(blank=True, null=True)
    class Meta:
        verbose_name_plural = "Saratani Users"