from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from wagtail.models import Page, Locale
from home.models import HomePage, Category, Product
from home.tools.tools_lib import build_slug_from_hierarchy


# @receiver(post_save)
# def set_show_in_menus_on_create(sender, instance, created, **kwargs):
#     if created and not instance.show_in_menus and instance.locale.language_code == 'ru':
#         instance.show_in_menus = True
#         instance.save()


@receiver(pre_save)
def auto_slug_all(sender, instance, **kwargs):
    if not isinstance(instance, Page) or instance.slug:
        return
    parent = instance.get_parent()
    if not parent:
        return
    lang = instance.locale.language_code.split('-')[0]
    slug = build_slug_from_hierarchy(instance, lang=lang) or instance.title.lower().replace(" ", "-")
    instance.slug = slug


@receiver(post_save)
def auto_translate(sender, instance, created, **kwargs):
    if not isinstance(instance, (Category, Product)):  # Исключаем HomePage
        return
    print(f"[SIGNAL] instance: {instance.title} ({instance.locale.language_code})")
    print("↳ parent:", instance.get_parent())
    source_lang = instance.locale.language_code
    target_langs = ['en', 'sr', 'ru']
    target_langs.remove(source_lang)

    domestije = Page.objects.filter(slug='domestije', depth=2).first()
    if not domestije:
        print("⚠️ Domestije page not found")
        return
    for code in target_langs:
        locale = Locale.objects.get(language_code=code)
        existing = Page.objects.filter(translation_key=instance.translation_key, locale=locale).first()
        if existing:
            # Обновляем существующую страницу
            existing.title = instance.title
            if hasattr(existing, 'description') and hasattr(instance, 'description'):
                existing.description = instance.description
            if hasattr(existing, 'image') and hasattr(instance, 'image'):
                existing.image = instance.image
            existing.slug = build_slug_from_hierarchy(existing, lang=code)
            existing.save_revision().publish()
            print(f"Updated {code} translation: {existing.title}")
        else:
            # Создаем новую переводную страницу
            home = HomePage.objects.filter(locale=locale, slug=code, depth=3).first()
            if not home:
                print(f"⚠️ HomePage not found for {code}")
                continue
            translated = instance.copy_for_translation(locale=locale, copy_parents=False)
            translated.title = instance.title
            if hasattr(translated, 'description'):
                translated.description = getattr(instance, 'description', '')
            if hasattr(translated, 'image'):
                translated.image = getattr(instance, 'image', None)
            translated.slug = build_slug_from_hierarchy(translated, lang=code)
            translated.save_revision().publish()
            translated.move(home, pos='last-child')  # Привязываем к HomePage (en, ru, sr)
            print(f"Created {code} translation: {translated.title}")