from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteConfiguration, Category, Destination, Expedition,
    FeaturedMedia, Booking, Article, QuickLead
)

# ── Admin Site Customization ───────────────────────────────────────────────────
admin.site.site_header = "The Editorial Expedition — Admin"
admin.site.site_title = "Otara Admin Panel"
admin.site.index_title = "📋 Content Management Panel"


# ── Site Configuration ─────────────────────────────────────────────────────────
@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'whatsapp_number')
    fieldsets = (
        ("🏷️ Branding & Contact", {
            "fields": ("site_name", "contact_email", "physical_address", "whatsapp_number"),
        }),
        ("🖼️ Hero Section", {
            "fields": ("hero_image", "hero_title", "hero_subtitle"),
            "description": "მთავარი გვერდის Hero სექციის კონტენტი",
        }),
        ("🌍 Top Destinations Section", {
            "fields": ("top_destinations_title", "top_destinations_subtitle"),
        }),
        ("🗺️ Tours Section", {
            "fields": ("tours_section_title", "tours_section_empty"),
        }),
        ("📄 About Page", {
            "fields": ("about_title", "about_subtitle", "philosophy_title", "philosophy_content"),
        }),
        ("📝 Footer & SEO", {
            "fields": ("about_text", "seo_description"),
        }),
        ("🔗 Social Links", {
            "fields": ("facebook_url", "instagram_url", "linkedin_url"),
            "classes": ("collapse",),
        }),
        ("🤖 Telegram Bot Notifications", {
            "fields": ("telegram_bot_token", "telegram_chat_id"),
            "classes": ("collapse",),
            "description": "Telegram Bot Token (@BotFather-დან) და Chat ID ნოტიფიკაციებისთვის.",
        }),
    )

    def has_add_permission(self, request):
        """მხოლოდ ერთი კონფიგურაცია შეიძლება არსებობდეს."""
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """წაშლა შეუძლებელია — საიტი გათიშვის რისკი."""
        return False

    def changelist_view(self, request, extra_context=None):
        """თუ არსებობს კონფიგურაცია, პირდაპირ რედაქტირებაზე გადავიდეს."""
        from django.shortcuts import redirect
        obj = self.model.objects.first()
        if obj:
            return redirect('admin:core_siteconfiguration_change', obj.pk)
        return super().changelist_view(request, extra_context)


# ── Category ───────────────────────────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


# ── Destination ────────────────────────────────────────────────────────────────
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'image_preview', 'is_top_destination')
    list_filter = ('is_top_destination',)
    search_fields = ('name', 'region')
    ordering = ('name',)
    list_editable = ('is_top_destination',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:70px;height:45px;object-fit:cover;border-radius:6px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"


# ── Expedition ─────────────────────────────────────────────────────────────────
@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'category', 'location', 'price', 'duration_days', 'is_featured')
    list_filter = ('category', 'location', 'is_featured')
    search_fields = ('title', 'description')
    list_editable = ('is_featured', 'price')
    ordering = ('-is_featured', 'title')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:50px;object-fit:cover;border-radius:6px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"


# ── Featured Media ─────────────────────────────────────────────────────────────
@admin.register(FeaturedMedia)
class FeaturedMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'video_file', 'video_url')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:120px;height:60px;object-fit:cover;border-radius:6px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Thumbnail Preview"


# ── Booking Bulk Actions ───────────────────────────────────────────────────────
@admin.action(description="✅ Mark selected as Confirmed")
def mark_confirmed(modeladmin, request, queryset):
    queryset.update(status="confirmed")


@admin.action(description="❌ Mark selected as Cancelled")
def mark_cancelled(modeladmin, request, queryset):
    queryset.update(status="cancelled")


# ── Booking ────────────────────────────────────────────────────────────────────
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'expedition', 'travel_date', 'group_size', 'total_price', 'status', 'created_at')
    list_filter   = ('status', 'travel_date', 'expedition')
    search_fields = ('full_name', 'user__username', 'expedition__title')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at', 'total_price')
    list_editable = ('status',)
    actions = [mark_confirmed, mark_cancelled]
    autocomplete_fields = ['expedition']
    raw_id_fields = ('user',)


# ── Article ────────────────────────────────────────────────────────────────────
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'image_preview', 'created_at')
    search_fields = ('title', 'content', 'category')
    list_filter   = ('category', 'created_at')
    ordering      = ('-created_at',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:50px;object-fit:cover;border-radius:6px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"


# ── Quick Lead ─────────────────────────────────────────────────────────────────
@admin.register(QuickLead)
class QuickLeadAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'phone_number', 'notes', 'created_at')
    search_fields = ('full_name', 'phone_number')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at',)
