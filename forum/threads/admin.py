from django.contrib import admin
from threads.models import Thread


class ThreadAdmin(admin.ModelAdmin):
    list_filter = ('pool', 'creator',)
    list_display = ('title', 'pool', 'description', 'creator')


admin.site.register(Thread, ThreadAdmin)
