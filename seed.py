import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import SiteConfiguration, Category, Destination, Expedition, FeaturedMedia

# 1. SiteConfig
site, _ = SiteConfiguration.objects.get_or_create(
    id=1,
    defaults=dict(
        hero_title="Unveiling the Soul of the Caucasus",
        hero_subtitle="Curated expeditions through Georgia's ancient valleys, hidden vineyards, and monolithic peaks.",
        about_text="A boutique travel studio specializing in deep-culture and high-adventure immersion across the Georgian Caucasus.",
        whatsapp_number="+995 555 010 203",
    )
)

# 2. Categories — WITH descriptions now
c1, _ = Category.objects.get_or_create(name="Trekking",
    defaults=dict(icon_name="hiking", description="Multi-day alpine routes"))
c2, _ = Category.objects.get_or_create(name="Wine & Culture",
    defaults=dict(icon_name="wine_bar", description="Qvevri tastings & cellar tours"))
c3, _ = Category.objects.get_or_create(name="Cultural",
    defaults=dict(icon_name="menu_book", description="History, art & local life"))
c4, _ = Category.objects.get_or_create(name="Photography",
    defaults=dict(icon_name="camera", description="Scenic landscape shoots"))

# 3. Destinations
d1, _ = Destination.objects.get_or_create(name="Kakheti",
    defaults=dict(region="East Georgia — Wine Country"))
d2, _ = Destination.objects.get_or_create(name="Svaneti",
    defaults=dict(region="Highlands — Medieval Towers"))
d3, _ = Destination.objects.get_or_create(name="Tbilisi",
    defaults=dict(region="Capital — Art & Architecture"))
d4, _ = Destination.objects.get_or_create(name="Kazbegi",
    defaults=dict(region="North — Epic Mountain Range"))

# 4. Featured Media
FeaturedMedia.objects.get_or_create(
    title="Drone Scenes — Georgian Highlands",
    defaults=dict(video_url="")
)

# 5. Expeditions
Expedition.objects.get_or_create(
    title="The Wine & Monasteries Journey",
    defaults=dict(
        description="Trace the 8,000-year roots of viticulture through Kakheti's legendary vineyards and explore UNESCO World Heritage monasteries on a journey through Georgia's spiritual and culinary heart.",
        price=450, duration_days=5, category=c2, location=d1, is_featured=True,
    )
)

Expedition.objects.get_or_create(
    title="High Caucasus Crests",
    defaults=dict(
        description="A demanding multi-day trek through Tusheti and Khevsureti's untamed alpine wilderness. Cross ancient passes, camp beneath the stars, and share tea with highland shepherds far from any road.",
        price=890, duration_days=8, category=c1, location=d2, is_featured=True,
    )
)

Expedition.objects.get_or_create(
    title="Tbilisi: Art, Sulfur & Old Town",
    defaults=dict(
        description="A curated 3-day urban immersion into the soulful Georgian capital. Explore hidden courtyards, sulphur bathhouses, the Narikala fortress, and dine at the best local restaurants with a cultural guide.",
        price=320, duration_days=3, category=c3, location=d3, is_featured=True,
    )
)

Expedition.objects.get_or_create(
    title="Kazbegi & Gergeti Trinity",
    defaults=dict(
        description="Ascend to 2,170m where the iconic Gergeti Trinity Church stands sentinel over the Dariali Gorge and Mount Kazbek. A 4-day journey into Georgia's most dramatic mountain landscape with expert local guides.",
        price=550, duration_days=4, category=c1, location=d4, is_featured=True,
    )
)

print('✅ Database seeded successfully with full data!')
print(f'   Categories: {Category.objects.count()}')
print(f'   Destinations: {Destination.objects.count()}')
print(f'   Expeditions: {Expedition.objects.count()}')
