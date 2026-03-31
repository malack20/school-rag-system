from django.db import models

class AnalyticsRecord(models.Model):
    metric = models.CharField(max_length=64)
    value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
