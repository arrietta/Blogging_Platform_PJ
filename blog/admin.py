from django.contrib import admin
from .models import Post, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'likes_count')
    list_filter = ('author',)
    search_fields = ('title', 'author__username')

    def likes_count(self, obj):
        return obj.likes.count()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
