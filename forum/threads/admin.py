from django.contrib import admin
from threads.models import Thread


class ThreadAdmin(admin.ModelAdmin):
    list_filter = ('pool',)
    list_display = ('title', 'description', 'pool')


admin.site.register(Thread, ThreadAdmin)
