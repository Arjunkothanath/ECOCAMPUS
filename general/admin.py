from django.contrib import admin
from .models import Bin
from .models import Feedback
from .models import BinCollection

@admin.register(BinCollection)
class BinCollectionAdmin(admin.ModelAdmin):
    list_display = ('bin', 'collected_by', 'collected_at')
    list_filter = ('collected_at',)
admin.site.register(Bin)
admin.site.register(Feedback)
