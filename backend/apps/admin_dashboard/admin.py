from django.contrib import admin
from .models import AnalyticsRecord

@admin.register(AnalyticsRecord)
class AnalyticsRecordAdmin(admin.ModelAdmin):
    list_display = ("metric", "value", "created_at")
