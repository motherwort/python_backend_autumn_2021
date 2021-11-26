from django.contrib import admin
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    list_filter = ('created', 'user', 'thread')
    list_display = ('user', 'content', 'thread')


admin.site.register(Post, PostAdmin)
