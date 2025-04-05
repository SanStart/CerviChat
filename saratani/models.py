import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class Prediction(models.Model):
    ide          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    patient_name = models.CharField(max_length=250, blank=True, null=True)
    patient_id   = models.CharField(max_length=250, blank=True, null=True)
    image        = models.ImageField(blank=True, null=True, default='th.jpeg', upload_to='predictions/')
    feature      = models.CharField(max_length=250, blank=True, null=True)
    f_value      = models.CharField(max_length=250, blank=True, null=True)
    results      = models.JSONField(blank=True, null=True)
    f_name       = models.CharField(max_length=250, blank=True, null=True)
    predicted    = models.BooleanField(default=False)
    date_scanned = models.DateTimeField(default=timezone.now)