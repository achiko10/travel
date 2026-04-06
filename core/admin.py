from django.contrib import admin
from .models import SiteConfiguration, Category, Destination, Expedition, FeaturedMedia, Booking, Article


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'whatsapp_number')
    # Only allow one instance of Site Configuration to exist
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ('user', 'expedition', 'full_name', 'travel_date', 'group_size', 'total_price', 'status', 'created_at')
    list_filter   = ('status', 'travel_date', 'expedition')
    search_fields = ('full_name', 'user__username', 'expedition__title')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at', 'total_price')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'content', 'category')
    list_filter = ('category', 'created_at')


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'price', 'duration_days', 'is_featured')
    list_filter = ('category', 'location', 'is_featured')
    search_fields = ('title', 'description')


admin.site.register(Category)
admin.site.register(Destination)
admin.site.register(FeaturedMedia)
