from django.contrib import admin

from admin_panel.models import BlogPost


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('created_at',)
    search_fields = ('title', 'blocks__text',)
