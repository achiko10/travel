from django.db import models
from django.contrib.auth.models import User

class SiteConfiguration(models.Model):
    # Branding
    site_name = models.CharField(max_length=100, default="The Editorial Expedition")
    contact_email = models.EmailField(default="hello@editorialexpedition.com")
    physical_address = models.CharField(max_length=255, default="Tbilisi, Georgia")
    whatsapp_number = models.CharField(max_length=20, default="+995 555 010 203")
    
    # Hero Section
    hero_title = models.CharField(max_length=255, default="Unveiling the Soul of the Caucasus")
    hero_subtitle = models.TextField(default="Curated expeditions through Georgia's ancient valleys, hidden vineyards, and monolithic peaks.")
    hero_image_url = models.URLField(max_length=500, help_text="Background image URL for the hero section")
    
    # About Page (New Dynamic Fields)
    about_title = models.CharField(max_length=255, default="About The Expedition")
    about_subtitle = models.TextField(default="We are an independent, boutique travel studio dedicated to curating unparalleled deep-culture immersions across the Georgian Caucasus.")
    philosophy_title = models.CharField(max_length=255, default="Our Philosophy")
    philosophy_content = models.TextField(default="We reject the mass-market approach to tourism. The Caucasus is not a checklist of monuments; it is a profound tapestry of ancient wisdom, rugged landscapes, and an unbroken lineage of hospitality.")
    
    # Footer & General
    about_text = models.TextField(default="A boutique travel studio specializing in deep-culture and high-adventure immersion across the Georgian Caucasus.")
    seo_description = models.TextField(max_length=300, default="High-end boutique travel and cultural expeditions across the Georgian Caucasus.", help_text="Site description for Google Search results.")
    
    # Social Links
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    # Telegram Bot Settings
    telegram_bot_token = models.CharField(max_length=255, blank=True, null=True, help_text="Bot Token from @BotFather")
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True, help_text="Target Chat ID for notifications")

    class Meta:
        verbose_name = "Global Site Branding & Settings"
        verbose_name_plural = "Global Site Branding & Settings"

    def __str__(self):
        return self.site_name


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=50, blank=True, help_text="Material symbol icon (e.g. 'hiking', 'wine_bar')")
    description = models.CharField(max_length=150, blank=True)
    
    class Meta:
        verbose_name = "Tour Type"
        verbose_name_plural = "Tour Types"

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., Kakheti, Svaneti")
    region = models.CharField(max_length=100, help_text="e.g., East Georgia, Highlands")
    image_url = models.URLField(max_length=500)
    is_top_destination = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Region & Location"
        verbose_name_plural = "Regions & Locations"

    def __str__(self):
        return f"{self.name} ({self.region})"


class Expedition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    duration_days = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.URLField(max_length=500)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tour & Expedition"
        verbose_name_plural = "Tours & Expeditions"

    def __str__(self):
        return self.title


class FeaturedMedia(models.Model):
    title = models.CharField(max_length=100, default="Homepage Drone Scenes")
    image_url = models.URLField(max_length=500)
    video_url = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name = "Homepage Video Banner"
        verbose_name_plural = "Homepage Video Banners"

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending — Awaiting Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='bookings')
    full_name  = models.CharField(max_length=200)
    travel_date = models.DateField()
    group_size  = models.PositiveIntegerField(default=1)
    total_price = models.IntegerField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"{self.user.username} → {self.expedition.title} ({self.travel_date})"


class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, help_text="e.g. Field Notes, Culture & Heritage", default="Dispatch")
    content = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        return self.title


class QuickLead(models.Model):
    full_name    = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    notes        = models.TextField(blank=True, null=True, help_text="Tour preference or specific question")
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Home Page Lead"
        verbose_name_plural = "Home Page Leads"

    def __str__(self):
        return f"{self.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
