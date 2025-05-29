from django.contrib import admin
from .models import ContactMessage
from django.utils.html import format_html

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'display_image')
    search_fields = ('name', 'email', 'subject', 'message')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'