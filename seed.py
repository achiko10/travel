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
        hero_image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuBoJyvC6JISUH2X3UsrQS-jVVCS7JHAIVQIFz274NpAje522P6uHCDiOMpviGHPnpg0lKBdoVbc_ICWGwZdN34_5SmhVhDdjyikC9uFb0Um7BbI8JrdYT6EZmdsAp7GMRQ4KEQIM-J48bSUnyQ4YRQggt90HooZ3P8X7yjcltfKr8Nqd-noWwKUjD_wMwscPM5JrdB10kiAbFO39Yj-GLU-R02vG0kgXkpYfzLLLOgjxvf_bJNXP4l7oJSKb6yZOVuzhZ6qL5VzVUcc",
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
    defaults=dict(region="East Georgia — Wine Country",
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuAsSMSp0I5X4i4dXlOYfWwc9_XRBPZ_qlMIc8YnWjdzCdsMa3A6c_YTzf2vuZ4pPn4YXuvvZJkjvXyXrKjMXx42oV9SaAtmC34mqnKYmbv-szAh_-hOiU-4ysDpdytk9jT1FtU3042TSruINBmOTNfZEvMPxszFGatMG6GGXRp4ieiL-WUmqZhM8wG5wHJ_uzEUWsItGsSE1Ah3MjNS-j_JdZj1uJt4p_DMKz2Cu_szPH2-vAW6hW0svX9UdVrFCwLPKKQfn4_IJ2pC"))
d2, _ = Destination.objects.get_or_create(name="Svaneti",
    defaults=dict(region="Highlands — Medieval Towers",
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuAuJddAJof8OfBEwJG4EgakHaASetixacM_O_fNO0zME238SBibnZ87EsQdwr63ZlSOcp02zf2yZPYI8rg6LFSrM9-2xr2BWkXnuOdqt_6NEAvfrh7Kwc5C31KSHjSLR1FKejxaHAddbL5JBT2AA4ZtXx8kcLGEe6QDoVxXGfo2CzRGkrfCG0bdO5HXp2AKbTdxNEBjPgAIAdEdSEnTxMDg9UxzY2BEh5HY8CPxWXMoNJrkyAV3B2EwcEN4X-pTtfJmIC-r7eMQrkkt"))
d3, _ = Destination.objects.get_or_create(name="Tbilisi",
    defaults=dict(region="Capital — Art & Architecture",
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuDywMSs3VF42-S2iKLdPXSjBET2VRb76vvfLSNzF0gRxSWHI1WAomUMr5bft4iKjVMNg079sZDbqWAPTrDFjJTiFE0TIhGwkNSYhq0uzyj66-3OBJFzUMzsGogkb4mApMH8avJKkxrhI-UKT1ox9B5y7aD-ZFGr5nLZw1CA-i4IEm9QslQkKY974OUPsnbp1hBBMx1LA_2mc-z1UjJHG7rMm9ER7GfRV5eTqjSpmMUG5ucZ8CtoW3nEvMgP--ygIjN7ASfmC4MYli4q"))
d4, _ = Destination.objects.get_or_create(name="Kazbegi",
    defaults=dict(region="North — Epic Mountain Range",
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuADvNLKeVg-Ccg3ENTJnI1m92lQK8gq-NlncH_D1laPL-xIDewxrClyR2w-h3O2IUOHSqo7_5tVNu9wjQoSfeS-hDbZ-Y-XRuLkhCFyAlXka2oMeMfQ7bLWpgkD9q2Cd3brIL3b9JIFCWIPICKk9DWBqWfCpcN7UPwhnNfCNn8nGikmhj6iD2WJXFg0h7NXufhgNxrRGDkP8meya-c40y95zbc2IUUkwsfEe6bSJ00GLIBPywv3SacL2foDxkO0H3rU8zaKxwq-G0kq"))

# 4. Featured Media
FeaturedMedia.objects.get_or_create(
    title="Drone Scenes — Georgian Highlands",
    defaults=dict(image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCfYK96kRC-Ge-v-U6DxL_58zdQdpiT7gSpG9gHgMx4J5E07mETZI5ySDC4dx-enPUMOnRgkXIB_zL9lHF5kSgyBwHVf3V4oLJ4nS_ZieQUZmI-VzlQflpe0ZP1q4Gs2uWcxLjOhhDSRmR4x2y7dLweygtLoSMpD8vUUGBCRR5hfXee1J6LFBpwetJoCfeagR_yG45hrevhV7pgo9RukgvsQmB5MTEsmYG_u_QlrsQ9TcRyc30zIctEzg5W3wIc65Jn8ajTSHNIZNin",
        video_url="")
)

# 5. Expeditions
Expedition.objects.get_or_create(
    title="The Wine & Monasteries Journey",
    defaults=dict(
        description="Trace the 8,000-year roots of viticulture through Kakheti's legendary vineyards and explore UNESCO World Heritage monasteries on a journey through Georgia's spiritual and culinary heart.",
        price=450, duration_days=5, category=c2, location=d1, is_featured=True,
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuDOu9PjOhuQu60-DJl7RnGe7rY2oiFPcT9sDmRrihQDW7e-3qj-ZlVdkgK8AXxsTGu47G_k3n2bVZlRuuHU-oWZGtqfAq6PHkJeRhozo7QA_GViBnmE3kpSAMVNpfC6pVH1wzyYw8d3l-8SOMItMPT76_T4qGZe2sAvrLcR3ZPsbbbQ1o4Gm0_ZVkmromLajrG2cN2CZ3uM2aobxY69LC-z5niBxOuyae7-_3cIrbaQGZQNnQO8pGCDee0D870DKcwNighVpkXfETSZ"
    )
)

Expedition.objects.get_or_create(
    title="High Caucasus Crests",
    defaults=dict(
        description="A demanding multi-day trek through Tusheti and Khevsureti's untamed alpine wilderness. Cross ancient passes, camp beneath the stars, and share tea with highland shepherds far from any road.",
        price=890, duration_days=8, category=c1, location=d2, is_featured=True,
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuBCSET0hFU1KlUfGEL9A1b6WN3rn5s2mP54HtXSyVXCV74bWdMbKnIQm8PzTlbR8Y5ezratowPn1O1yzD_PG--a5-MpljfpkGnLn9VcYh_eboNKz0Xg_l-H-0miaq7af35Up8LycqbrZEud8epRv4c5EA7leSAC4jOsHGiPHleY6qOCSnomgpM7XrOLWlcssR9qD3Eq5D2Xqh6kzSzIXgQV9d2Ay3_AZhwmBxBDOgwwD6bt8_Bfe0SmyT2xuYFi1IdePrSnemmUDbJj"
    )
)

Expedition.objects.get_or_create(
    title="Tbilisi: Art, Sulfur & Old Town",
    defaults=dict(
        description="A curated 3-day urban immersion into the soulful Georgian capital. Explore hidden courtyards, sulphur bathhouses, the Narikala fortress, and dine at the best local restaurants with a cultural guide.",
        price=320, duration_days=3, category=c3, location=d3, is_featured=True,
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuDywMSs3VF42-S2iKLdPXSjBET2VRb76vvfLSNzF0gRxSWHI1WAomUMr5bft4iKjVMNg079sZDbqWAPTrDFjJTiFE0TIhGwkNSYhq0uzyj66-3OBJFzUMzsGogkb4mApMH8avJKkxrhI-UKT1ox9B5y7aD-ZFGr5nLZw1CA-i4IEm9QslQkKY974OUPsnbp1hBBMx1LA_2mc-z1UjJHG7rMm9ER7GfRV5eTqjSpmMUG5ucZ8CtoW3nEvMgP--ygIjN7ASfmC4MYli4q"
    )
)

Expedition.objects.get_or_create(
    title="Kazbegi & Gergeti Trinity",
    defaults=dict(
        description="Ascend to 2,170m where the iconic Gergeti Trinity Church stands sentinel over the Dariali Gorge and Mount Kazbek. A 4-day journey into Georgia's most dramatic mountain landscape with expert local guides.",
        price=550, duration_days=4, category=c1, location=d4, is_featured=True,
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuADvNLKeVg-Ccg3ENTJnI1m92lQK8gq-NlncH_D1laPL-xIDewxrClyR2w-h3O2IUOHSqo7_5tVNu9wjQoSfeS-hDbZ-Y-XRuLkhCFyAlXka2oMeMfQ7bLWpgkD9q2Cd3brIL3b9JIFCWIPICKk9DWBqWfCpcN7UPwhnNfCNn8nGikmhj6iD2WJXFg0h7NXufhgNxrRGDkP8meya-c40y95zbc2IUUkwsfEe6bSJ00GLIBPywv3SacL2foDxkO0H3rU8zaKxwq-G0kq"
    )
)

print('✅ Database seeded successfully with full data!')
print(f'   Categories: {Category.objects.count()}')
print(f'   Destinations: {Destination.objects.count()}')
print(f'   Expeditions: {Expedition.objects.count()}')
