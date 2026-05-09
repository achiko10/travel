from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from tinymce.models import HTMLField


class SiteConfiguration(models.Model):
    # Branding
    site_name = models.CharField(max_length=100, default="The Editorial Expedition", verbose_name="საიტის სახელი (Site Name)")
    contact_email = models.EmailField(default="hello@editorialexpedition.com", verbose_name="საკონტაქტო ელ-ფოსტა (Contact Email)")
    physical_address = models.CharField(max_length=255, default="Tbilisi, Georgia", verbose_name="მისამართი (Physical Address)")
    whatsapp_number = models.CharField(max_length=20, default="+995 555 010 203", verbose_name="WhatsApp ნომერი (WhatsApp Number)")

    # Hero Section
    hero_title = models.CharField(max_length=255, default="Unveiling the Soul of the Caucasus", verbose_name="მთავარი სათაური (Hero Title)")
    hero_subtitle = models.TextField(default="Curated expeditions through Georgia's ancient valleys, hidden vineyards, and monolithic peaks.", verbose_name="მთავარი ქვესათაური (Hero Subtitle)")
    hero_image = models.ImageField(
        upload_to='hero/',
        blank=True, null=True,
        help_text="ატვირთეთ Hero სექციის ფონური სურათი",
        verbose_name="მთავარი ფოტოსურათი (Hero Image)"
    )

    # Top Destinations Section
    top_destinations_title = models.CharField(max_length=255, default="Top Destinations", verbose_name="ტოპ დესტინაციების სათაური (Top Destinations Title)")
    top_destinations_subtitle = models.CharField(max_length=255, default="The quintessential Georgian experience", verbose_name="ტოპ დესტინაციების ქვესათაური (Top Destinations Subtitle)")

    # Expeditions Section
    tours_section_title = models.CharField(max_length=255, default="Curated Expeditions", verbose_name="ტურების სექციის სათაური (Tours Section Title)")
    tours_section_empty = models.CharField(max_length=255, default="No Expeditions Found", verbose_name="ტურების სექცია - როცა ტური არ მოიძებნა (Tours Empty State)")

    # About Page
    about_title = models.CharField(max_length=255, default="About The Expedition", verbose_name="ჩვენს შესახებ სათაური (About Title)")
    about_subtitle = models.TextField(default="We are an independent, boutique travel studio dedicated to curating unparalleled deep-culture immersions across the Georgian Caucasus.", verbose_name="ჩვენს შესახებ ქვესათაური (About Subtitle)")
    philosophy_title = models.CharField(max_length=255, default="Our Philosophy", verbose_name="ფილოსოფიის სათაური (Philosophy Title)")
    philosophy_content = HTMLField(default="We reject the mass-market approach to tourism...", verbose_name="ფილოსოფიის ტექსტი (Philosophy Content)")

    # Footer & General
    about_text = models.TextField(default="A boutique travel studio specializing in deep-culture and high-adventure immersion across the Georgian Caucasus.", verbose_name="ფუტერის ტექსტი (Footer Text)")
    seo_description = models.TextField(max_length=300, default="High-end boutique travel and cultural expeditions across the Georgian Caucasus.", help_text="Site description for Google Search results.", verbose_name="SEO აღწერა (SEO Description)")

    # Social Links
    facebook_url = models.URLField(blank=True, null=True, verbose_name="Facebook ლინკი (Facebook URL)")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="Instagram ლინკი (Instagram URL)")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="LinkedIn ლინკი (LinkedIn URL)")

    # Telegram Bot Settings
    telegram_bot_token = models.CharField(max_length=255, blank=True, null=True, help_text="Bot Token from @BotFather", verbose_name="ტელეგრამ ბოტის ტოკენი (Telegram Bot Token)")
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True, help_text="Target Chat ID for notifications", verbose_name="ტელეგრამ ჩატის ID (Telegram Chat ID)")

    class Meta:
        verbose_name = "საიტის გლობალური პარამეტრები (Global Site Settings)"
        verbose_name_plural = "საიტის გლობალური პარამეტრები (Global Site Settings)"

    def __str__(self):
        return self.site_name


class Category(models.Model):
    ICON_CHOICES = [
        ('map', 'Map'),
        ('hiking', 'Hiking'),
        ('wine_bar', 'Wine Bar'),
        ('directions_car', 'Car / Offroad'),
        ('church', 'Church / Culture'),
        ('restaurant', 'Restaurant / Food'),
        ('hotel', 'Hotel / Accommodation'),
        ('photo_camera', 'Photography'),
        ('landscape', 'Landscape'),
        ('forest', 'Forest / Nature'),
        ('explore', 'Explore'),
    ]
    name = models.CharField(max_length=100, verbose_name="სახელი (Name)")
    icon_name = models.CharField(max_length=50, blank=True, choices=ICON_CHOICES, help_text="Material symbol icon (e.g. 'hiking', 'wine_bar')", verbose_name="აიქონი (Icon)")
    description = models.CharField(max_length=150, blank=True, verbose_name="მოკლე აღწერა (Short Description)")

    class Meta:
        verbose_name = "ტურის კატეგორია (Tour Type)"
        verbose_name_plural = "ტურის კატეგორიები (Tour Types)"
        ordering = ['name']

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., Kakheti, Svaneti", verbose_name="სახელი (Name)")
    region = models.CharField(max_length=100, help_text="e.g., East Georgia, Highlands", verbose_name="რეგიონი (Region)")
    image = models.ImageField(
        upload_to='destinations/',
        blank=True, null=True,
        help_text="ატვირთეთ დესტინაციის სურათი",
        verbose_name="სურათი (Image)"
    )
    is_top_destination = models.BooleanField(default=True, verbose_name="არის ტოპ დესტინაცია? (Is Top Destination?)")

    class Meta:
        verbose_name = "რეგიონი და დესტინაცია (Region & Location)"
        verbose_name_plural = "რეგიონები და დესტინაციები (Regions & Locations)"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.region})"


class Expedition(models.Model):
    title = models.CharField(max_length=200, verbose_name="სათაური (Title)")
    description = HTMLField(verbose_name="აღწერა (Description)")
    price = models.IntegerField(verbose_name="ფასი (Price)")
    duration_days = models.IntegerField(verbose_name="ხანგრძლივობა დღეებში (Duration in Days)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="კატეგორია (Category)")
    location = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ლოკაცია (Location)")
    image = models.ImageField(
        upload_to='expeditions/',
        blank=True, null=True,
        help_text="ატვირთეთ ტური-ს მთავარი სურათი",
        verbose_name="მთავარი სურათი (Main Image)"
    )
    is_featured = models.BooleanField(default=True, verbose_name="გამოჩნდეს მთავარ გვერდზე? (Is Featured?)")

    class Meta:
        verbose_name = "ტური და ექსპედიცია (Tour & Expedition)"
        verbose_name_plural = "ტურები და ექსპედიციები (Tours & Expeditions)"

    def __str__(self):
        return self.title


class FeaturedMedia(models.Model):
    title = models.CharField(max_length=100, default="Homepage Drone Scenes", verbose_name="სათაური (Title)")
    image = models.ImageField(
        upload_to='featured/',
        blank=True, null=True,
        help_text="ატვირთეთ Thumbnail სურათი (ვიდეო ბანერის ფონი)",
        verbose_name="ფონური სურათი (Thumbnail Image)"
    )
    video_file = models.FileField(
        upload_to='videos/',
        blank=True, null=True,
        help_text="ატვირთეთ ვიდეო ფაილი (MP4) პირდაპირ.",
        verbose_name="ვიდეო ფაილი (Video File)"
    )
    video_url = models.URLField(
        max_length=500, 
        blank=True, 
        help_text="ან ჩასვით YouTube/Vimeo ლინკი (თუ ვიდეო ფაილს არ ტვირთავთ)",
        verbose_name="ვიდეოს ლინკი (Video URL)"
    )

    class Meta:
        verbose_name = "მთავარი გვერდის ვიდეო (Homepage Video Banner)"
        verbose_name_plural = "მთავარი გვერდის ვიდეოები (Homepage Video Banners)"

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending — Awaiting Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="მომხმარებელი (User)")
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='bookings', verbose_name="ტური (Expedition)")
    full_name  = models.CharField(max_length=200, verbose_name="სრული სახელი (Full Name)")
    travel_date = models.DateField(verbose_name="მოგზაურობის თარიღი (Travel Date)")
    group_size  = models.PositiveIntegerField(default=1, verbose_name="ჯგუფის ზომა (Group Size)")
    total_price = models.IntegerField(verbose_name="ჯამური ფასი (Total Price)")
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="სტატუსი (Status)")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="შექმნის თარიღი (Created At)")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "ჯავშანი (Reservation)"
        verbose_name_plural = "ჯავშნები (Reservations)"

    def __str__(self):
        return f"{self.user.username} → {self.expedition.title} ({self.travel_date})"


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="სათაური (Title)")
    category = models.CharField(max_length=100, help_text="e.g. Field Notes, Culture & Heritage", default="Dispatch", verbose_name="კატეგორია (Category)")
    content = HTMLField(verbose_name="ტექსტი (Content)")
    image = models.ImageField(
        upload_to='articles/',
        blank=True, null=True,
        help_text="ატვირთეთ სტატიის მთავარი სურათი",
        verbose_name="მთავარი სურათი (Main Image)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="შექმნის თარიღი (Created At)")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "ბლოგის სტატია (Journal Entry)"
        verbose_name_plural = "ბლოგის სტატიები (Journal Entries)"

    def __str__(self):
        return self.title


class QuickLead(models.Model):
    full_name    = models.CharField(max_length=200, verbose_name="სრული სახელი (Full Name)")
    phone_number = models.CharField(max_length=50, verbose_name="ტელეფონის ნომერი (Phone Number)")
    notes        = models.TextField(blank=True, null=True, help_text="Tour preference or specific question", verbose_name="შენიშვნები/კითხვა (Notes)")
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name="შექმნის თარიღი (Created At)")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "მთავარი გვერდის მოთხოვნა (Home Page Lead)"
        verbose_name_plural = "მთავარი გვერდის მოთხოვნები (Home Page Leads)"

    def __str__(self):
        return f"{self.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
