from django.utils.text import slugify
from unidecode import unidecode
from wagtail.models import Page, Locale
from home.models import Category


def build_slug_from_hierarchy(instance, lang=None):
    # Получаем локаль (гарантировано существует)
    locale = Locale.objects.get(language_code=lang) if lang else instance.locale

    # Транслитерируем текущий заголовок
    current_slug_part = slugify(unidecode(instance.title.lower()))

    # Для depth < 5 — возвращаем slug текущей страницы
    if instance.depth < 5:
        return ensure_unique_slug(current_slug_part, instance, locale)

    # Для depth >= 5 — берём слаг родителя и комбинируем
    parent = instance.get_parent()
    if not parent:
        return ensure_unique_slug(current_slug_part, instance, locale)

    # Получаем локализованного родителя
    parent_in_locale = Page.objects.filter(
        translation_key=parent.translation_key,
        locale=locale
    ).first() or parent

    parent_slug = parent_in_locale.slug  # Берём готовый слаг родителя

    base_slug = f"{parent_slug}-{current_slug_part}"
    return ensure_unique_slug(base_slug, instance, locale)


def ensure_unique_slug(base_slug, instance, locale):
    """Гарантирует уникальность слага."""
    parent = instance.get_parent()
    if not parent:
        return base_slug

    parent_in_locale = Page.objects.filter(
        translation_key=parent.translation_key,
        locale=locale
    ).first() or parent

    counter = 1
    slug = base_slug
    while Page.objects.exclude(id=instance.id).filter(
            slug=slug,
            locale=locale,
            path__startswith=parent_in_locale.path
    ).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

def test_build_slug_from_hierarchy():
    for code in ['ru', 'en', 'sr']:
        locale = Locale.objects.get(language_code=code)
        categories = Category.objects.filter(locale=locale, depth__gte=4)
        for category in categories:
            slug = build_slug_from_hierarchy(category, lang=code)
            titles = []
            page = category
            while page.depth > 0:
                if page.depth >= 1:
                    titles.insert(0, page.title)
                parent = page.get_parent()
                if not parent or (parent and not hasattr(page, 'translation_key')):
                    break
                page = Page.objects.filter(translation_key=parent.translation_key, locale=locale).first() or parent
            print(
                f"Locale: {code}, Category: {category.title}, Depth: {category.depth}, Generated Slug: {slug}, Titles: {titles}")


def sync_locales():
    # Синхронизация translation_key
    ru_parent = Page.objects.filter(locale__language_code='ru', depth=3).first()
    if not ru_parent:
        print("RU parent not found")
    else:
        ru_translation_key = ru_parent.translation_key
        print(f"RU Translation Key: {ru_translation_key}")

        # Синхронизируем для en и sr
        for code in ['en', 'sr']:
            locale = Locale.objects.get(language_code=code)
            parent = Page.objects.filter(locale=locale, depth=3).first()
            if parent and parent.translation_key != ru_translation_key:
                parent.translation_key = ru_translation_key
                parent.save()
                parent.specific.save_revision().publish()
                print(f"Updated translation_key for {code}: {parent.translation_key}")
            elif not parent:
                print(f"No parent found for {code}")
            else:
                print(f"No update needed for {code}")


def test_sync_locales():
    # Проверка
    for code in ['ru', 'en', 'sr']:
        locale = Locale.objects.get(language_code=code)
        parent = Page.objects.filter(locale=locale, depth=3).first()
        if parent:
            print(f"Locale: {code}, Parent Title: {parent.title}, Slug: {parent.slug}, Translation Key: {parent.translation_key}")
        else:
            print(f"No parent found for locale {code}")

