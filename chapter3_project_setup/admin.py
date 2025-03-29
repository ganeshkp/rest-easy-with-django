from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import WatchList, StreamPlatform, Review

class WatchListAdmin(GuardedModelAdmin):
    pass

# Register your models here.
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(StreamPlatform)
admin.site.register(Review)