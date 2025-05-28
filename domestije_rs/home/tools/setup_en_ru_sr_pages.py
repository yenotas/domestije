
# =================================================
# ПОСЛЕ ЗАПУСКА ВЫПОЛНИТЬ python manage.py fixtree
# =================================================
import django
import os
import sys
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domestije_rs.settings.dev')
django.setup()

from wagtail.models import Page, Locale
from home.models import HomePage

locales = {
    'en': Locale.objects.get_or_create(language_code='en')[0],
    'ru': Locale.objects.get_or_create(language_code='ru')[0],
    'sr': Locale.objects.get_or_create(language_code='sr')[0],
}

# 1. Создаём корневую страницу Domestije (если её нет)
root = Page.get_first_root_node()
domestije = HomePage.objects.filter(title="Domestije", depth=2).first()
if not domestije:
    domestije = HomePage(title="Domestije", slug="domestije", locale=locales['en'])
    root.add_child(instance=domestije)
    domestije.save_revision().publish()
    print("✅ Создана корневая страница 'Domestije'")
else:
    print("✅ Страница 'Domestije' уже существует")

# 2. Создаём дочерние страницы для локалей
for code, title in [('en', 'English'), ('ru', 'Русский'), ('sr', 'Srpski')]:
    locale = locales[code]
    child = HomePage.objects.filter(title=title, locale=locale, path__startswith=domestije.path).first()
    if not child:
        page = HomePage(title=title, slug=code, locale=locale)
        domestije.add_child(instance=page)
        page.save_revision().publish()
        print(f"✅ Создана дочерняя страница {title} ({code})")
    else:
        print(f"✅ Уже есть страница {title} ({code})")



# Проверка на дублирующиеся slug-и
slugs = list(Page.objects.values_list('slug', flat=True))
duplicates = [s for s, count in Counter(slugs).items() if count > 1]

if duplicates:
    print("🚨 Конфликтующие slug-и:", duplicates)
else:
    print("✅ Уникальные slug-и")
