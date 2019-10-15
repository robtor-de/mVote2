from django.contrib import admin
from vmgr.models import SongRequest

class SongReqAdmin(admin.ModelAdmin):
    pass

admin.site.register(SongRequest, SongReqAdmin)
