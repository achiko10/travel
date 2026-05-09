# 🔧 Admin Panel — სრული გამოსწორების გეგმა
### პროექტი: Otara / The Editorial Expedition

---

## 🔴 მთავარი პრობლემა: ფოტოების ატვირთვა

**სად არის პრობლემა:** ყველა model-ი სადაც სურათი ჭირდება, გამოიყენება `URLField` — ანუ სისტემა ელის პირდაპირ URL-ს და **არ იძლევა ფაილის ატვირთვის საშუალებას**.

| Model | Field | ამჟამინდელი ტიპი | პრობლემა |
|---|---|---|---|
| `SiteConfiguration` | `hero_image_url` | `URLField` | ✗ URL ხელით |
| `Destination` | `image_url` | `URLField` | ✗ URL ხელით |
| `Expedition` | `image_url` | `URLField` | ✗ URL ხელით |
| `FeaturedMedia` | `image_url` | `URLField` | ✗ URL ხელით |
| `FeaturedMedia` | `video_url` | `URLField` | ✗ URL ხელით |
| `Article` | `image_url` | `URLField` | ✗ URL ხელით |

**გამოსწორება:** ყველა `URLField` → `ImageField` (ფოტოსთვის) + `FileField` (ვიდეოსთვის), `Pillow` პაკეტი + `MEDIA_ROOT/MEDIA_URL` settings-ში.

---

## 📋 ყველა პრობლემა — პრიორიტეტის მიხედვით

---

### 🔴 CRITICAL — მაუმუშავებელია

#### 1. ფოტო/მედია ატვირთვის სისტემა არ არსებობს
- `settings.py`-ში **`MEDIA_ROOT` და `MEDIA_URL` არ არის** → ფაილები სადაც შეინახება, განუსაზღვრელია
- `Pillow` **requirements.txt**-ში არ არის → `ImageField` ვერ იმუშავებს
- `config/urls.py`-ში **`static(MEDIA_URL, document_root=MEDIA_ROOT)`** არ არის → ატვირთული ფოტოები ვერ გამოჩნდება frontend-ზე

#### 2. `DEBUG = False` — Development-ზე static ფაილები ვერ იტვირთება
- `settings.py` line 44: `DEBUG = False` — ეს production-ის პარამეტრია
- Development-ზე ეს ნიშნავს: CSS/JS ვერ ჩაიტვირთება `manage.py runserver`-ით
- **შედეგი:** ადმინ პანელი ვიზუალურად გატეხილია (Django admin CSS არ იტვირთება)

#### 3. `settings.py`-ში ორი `from pathlib import Path` და ორი docstring
- ფაილი line 1-16 და line 19-34 — **გაორმაგებული კოდი** (დუბლიკატი)
- ეს შეიძლება გამოიწვიოს მოულოდნელი შეცდომები

---

### 🟠 HIGH — მნიშვნელოვანი ნაკლი

#### 4. Admin Panel — `Destination` და `Category` — ძველი `admin.site.register()`
```python
# admin.py line 38-40 — ძველი, კონტროლი ნაკლებია:
admin.site.register(Category)
admin.site.register(Destination)
admin.site.register(FeaturedMedia)
```
- **პრობლემა:** List display, search, filter არ არის კონფიგურირებული
- ადმინ ვერ ხედავს სიაში მთავარ ველებს, ვერ ეძებს, ვერ ფილტრავს

#### 5. `SiteConfiguration` Admin — ველები დაჯგუფებული არ არის
- ამჟამად ყველა ველი ერთ სიიად ჩნდება (Branding, Hero, About, Footer, Social, Telegram — ერთად)
- `fieldsets` არ არის → ადმინი ვერ ნავიგირებს ეფექტურად

#### 6. `Booking` — სტატუსის შეცვლა სიაში შეუძლებელია
- `list_editable` არ არის → სტატუსის შეცვლისთვის ყოველ ჯერ ცალკე booking-ი უნდა გაიხსნას
- `actions` (bulk approve/cancel) არ არის

#### 7. `QuickLead` Model — Admin-ში **საერთოდ არ არის რეგისტრირებული**
- `admin.py` line 2: `QuickLead` import-ში **არ ჩანს**
- ადმინ პანელში Home Page Lead-ების ნახვა **შეუძლებელია**!

#### 8. `Article` — Rich Text Editor არ არის
- `content = models.TextField()` — ჩვეულებრივი textarea
- მომხმარებელი ვერ ამატებს სათაურებს, bold-ს, სურათებს სტატიაში

---

### 🟡 MEDIUM — UX გაუმჯობესება

#### 9. `Expedition` — `description` — Rich Text Editor არ არის
- ტური-ს აღწერა plain textarea-ია
- ფორმატირება შეუძლებელია ადმინ პანელიდან

#### 10. `SiteConfiguration` — Singleton enforcement სრული არ არის
- `has_add_permission` გადაფარულია მაგრამ `has_delete_permission` **არ** არის გადაფარული
- ადმინ შეიძლება შემთხვევით წაშალოს ერთი კონფიგურაცია და ყველა გვერდი გათიშოს

#### 11. `Expedition` — ველი `image_url` (URLField) — Preview არ ჩანს admin-ში
- ადმინ ხედავს მხოლოდ URL ველს, სურათი preview-ში **არ ჩანს**
- ამ დროს მომხმარებელს არ ეცოდინება, სწორია ლინკი თუ არა

#### 12. Admin Panel Title — `Django Administration` ნაწილობრივ კასტომიზებულია
- `admin.site.site_header` არ არის დაყენებული
- ჩანს generic "Django Administration" სათაური

#### 13. `Booking` — `user` field — Select dropdown-ი ძალიან მოუხერხებელია
- ბევრი მომხმარებელი შემთხვევაში dropdown ძალიან გრძელია
- `raw_id_fields` ან `autocomplete_fields` არ არის

---

### 🟢 LOW — პატარა გაუმჯობესება

#### 14. `FeaturedMedia` — ვიდეო URL-ის Validation
- `video_url` ამ დროს ნებისმიერ URL-ს იღებს — YouTube, Vimeo, local — validation არ ვხდება

#### 15. `Category` — `icon_name` — Dropdown-ი კარგი იქნება
- ამ დროს ხელით ვწერთ icon სახელს, შეცდომის შანსი მაღალია

#### 16. Admin Ordering — List-ებში default ordering ნაწილობრივ გვაქვს
- `Category` და `Destination` — ordering არ არის განსაზღვრული

---

## ✅ გამოსასწორებელი ფაილები — გეგმა

### ნაბიჯი 1 — Media Upload სისტემა (🔴 CRITICAL)

**`requirements.txt`** → დაამატე `Pillow`

**`config/settings.py`** → გაასუფთავე დუბლიკატი + დაამატე:
```python
import os
DEBUG = True  # development-ზე
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**`config/urls.py`** → დაამატე media serving:
```python
from django.conf import settings
from django.conf.urls.static import static
# urlpatterns-ის ბოლოს:
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**`core/models.py`** → შეცვალე URLField → ImageField/FileField:
```python
# ყველა image_url → image (ImageField)
image = models.ImageField(upload_to='images/', blank=True, null=True)
# video_url → video_file (FileField) ან დატოვე URLField YouTube-ისთვის
```

---

### ნაბიჯი 2 — Admin Panel სრული გადაწყობა (🟠 HIGH)

**`core/admin.py`** → სრულად გადაიწეროს:
- `QuickLead` დაამატე import-ში და დაარეგისტრირე
- `Category`, `Destination`, `FeaturedMedia` → `@admin.register()` დეკორატორი + `list_display`, `search_fields`
- `SiteConfiguration` → `fieldsets` დაჯგუფება (Branding, Hero, About, Social, Telegram)
- `SiteConfiguration` → `has_delete_permission` → `return False`
- `Booking` → `list_editable = ('status',)` + bulk actions
- Admin site კასტომიზაცია: `admin.site.site_header`, `admin.site.site_title`

---

### ნაბიჯი 3 — Migration (🔴 CRITICAL)

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### ნაბიჯი 4 — Template-ების განახლება (medium)

ყველა template-ში სადაც `expedition.image_url` ან `destination.image_url` გამოიყენება:
```html
<!-- ძველი -->
<img src="{{ expedition.image_url }}">
<!-- ახალი -->
<img src="{{ expedition.image.url }}">
```

---

## 📊 შეჯამება

| # | პრობლემა | სირთულე | მნიშვნელობა |
|---|---|---|---|
| 1 | Media Upload (MEDIA_ROOT/URL) | საშუალო | 🔴 Critical |
| 2 | URLField → ImageField | მარტივი | 🔴 Critical |
| 3 | Pillow dependency | ძალიან მარტივი | 🔴 Critical |
| 4 | DEBUG=False (dev) | ძალიან მარტივი | 🔴 Critical |
| 5 | Settings.py დუბლიკატი | მარტივი | 🔴 Critical |
| 6 | QuickLead Admin-ში არ ჩანს | მარტივი | 🟠 High |
| 7 | Category/Destination Admin სუსტია | მარტივი | 🟠 High |
| 8 | SiteConfiguration fieldsets | მარტივი | 🟠 High |
| 9 | Booking list_editable status | მარტივი | 🟠 High |
| 10 | SiteConfiguration has_delete | ძალიან მარტივი | 🟠 High |
| 11 | Image preview admin-ში | საშუალო | 🟡 Medium |
| 12 | Admin panel title/branding | ძალიან მარტივი | 🟡 Medium |
| 13 | Template image URL-ების განახლება | მარტივი | 🟡 Medium |

**სულ: 13 პრობლემა**, რომელთაგან **5 Critical** და **5 High** პრიორიტეტულია.

---

> **შემდეგი ნაბიჯი:** გვითხარი, შევასრულო ყველა გამოსწორება ერთბაშად, თუ ეტაპობრივად?
