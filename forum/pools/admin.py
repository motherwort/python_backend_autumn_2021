from django.contrib import admin
from pools.models import Pool


class PoolAdmin(admin.ModelAdmin):
    list_filter = ('created', 'creator')
    list_display = ('name', 'created', 'creator')


admin.site.register(Pool, PoolAdmin)
