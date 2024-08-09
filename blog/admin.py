from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'likes', 'author', 'pub_date')
    search_fields = ('title',)
    filter_fields = ('pub_date',)
