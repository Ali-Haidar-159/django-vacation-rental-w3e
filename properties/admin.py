from django.contrib import admin
from .models import Location, Property, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'caption')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country', 'zip_code')
    search_fields = ('city', 'state', 'country')
    list_filter = ('country', 'state')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'bedrooms', 'bathrooms', 'price_per_night', 'location', 'created_at')
    list_filter = ('property_type', 'bedrooms', 'bathrooms')
    search_fields = ('name', 'description', 'location__city')
    inlines = [ImageInline]
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'property_type')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'max_guests', 'price_per_night')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('property__name', 'caption')
