from django.contrib import admin
from .models import Post, SideBar, Like, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'slug',
        'status',
        'date_created'
    )
    list_display_links = (
        'user',
        'title',
        'slug',
    )

    prepopulated_fields = {'slug': ('title',)}


@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'date_created', 'approved_comment')
    search_fields = ['author', 'content']


admin.site.register(Like)
