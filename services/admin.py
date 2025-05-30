from django.contrib import admin
from .models import Service, ServiceImage, Booking, WorkSpecification, Review, Reply

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ('image',)  # Updated to show URL field

class WorkSpecificationInline(admin.TabularInline):
    model = WorkSpecification
    extra = 1
    fields = ('name', 'price')

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1
    fields = ('user', 'comment', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceImageInline, WorkSpecificationInline]
    list_display = ('title', 'category')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'get_work_specifications', 'price', 'booking_date', 'booking_time', 'address', 'latitude', 'longitude', 'status', 'is_editable')
    list_filter = ('status', 'is_editable', 'booking_date')
    search_fields = ('user__username', 'service__title', 'address')

    def get_work_specifications(self, obj):
        return ", ".join(spec.name for spec in obj.work_specifications.all())
    get_work_specifications.short_description = 'Work Specifications'

class WorkSpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price')
    list_filter = ('service',)
    search_fields = ('name', 'service__title')

class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
    list_display = ('user', 'service', 'rating', 'comment', 'created_at', 'updated_at')
    list_filter = ('rating', 'service', 'created_at')
    search_fields = ('user__username', 'service__title', 'comment')

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'comment', 'created_at', 'updated_at')
    list_filter = ('review', 'created_at')
    search_fields = ('user__username', 'review__service__title', 'comment')

admin.site.register(Review, ReviewAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(WorkSpecification, WorkSpecificationAdmin)
admin.site.register(Reply, ReplyAdmin)