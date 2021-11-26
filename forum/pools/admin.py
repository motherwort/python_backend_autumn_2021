from django.contrib import admin
from pools.models import Pool


class PoolAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = ('name', 'created')


admin.site.register(Pool, PoolAdmin)
