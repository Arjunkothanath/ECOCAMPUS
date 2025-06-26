from django.contrib import admin
from general.models import Feedback

admin.site.unregister(Feedback)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'location', 'message', 'status', 'created_at')
