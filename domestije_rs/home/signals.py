# signals.py
import time
import threading
from django.db.models import CharField, TextField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from wagtail.fields import RichTextField
from wagtail.models import Page, Locale
from django.utils.text import slugify
from unidecode import unidecode
from home.models import HomePage, Category, Product, Recipe  # Убедитесь, что все ваши модели импортированы
from translate import Translator
from bs4 import BeautifulSoup, NavigableString
from django.utils import translation
from wagtail.rich_text import expand_db_html

# Лок для предотвращения рекурсии auto_translate в одном потоке
_auto_translate_processing_lock = threading.local()


def ensure_unique_slug(base_slug, instance, locale):
    original_slug = base_slug
    counter = 1

    while True:
        queryset = Page.objects.filter(slug=base_slug, locale=locale)

        # Исключаем текущий экземпляр, если он уже существует (т.е. обновляется)
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

        if not queryset.exists():
            break  # Если нет других страниц с таким слагом, выходим из цикла

        # Если такой слаг уже занят, генерируем новый и повторяем
        base_slug = f"{original_slug}-{counter}"
        counter += 1

    return base_slug


def build_slug_from_hierarchy(instance, lang=None):
    locale_obj = Locale.objects.get(language_code=lang) if lang else instance.locale
    current_slug_part = slugify(unidecode(instance.title.lower()))

    parent = instance.get_parent()

    # Если нет родителя, это корневая страница (например, HomePage или Category первого уровня).
    # Ее слаг - это просто ее собственное название.
    # Пример: для "Услуги" (depth 4), слаг должен быть "uslugi"
    if not parent:
        return ensure_unique_slug(current_slug_part, instance, locale_obj)

    # Для всех остальных страниц (с родителем), слаг должен быть составным:
    # слаг родителя + слаг текущей страницы.
    # Мы должны получить слаг родителя в целевой локали.
    parent_in_locale_base = Page.objects.filter(
        translation_key=parent.translation_key,
        locale=locale_obj
    ).first()

    parent_in_locale = parent_in_locale_base.specific if parent_in_locale_base else None

    parent_slug_for_hierarchy = ""
    if parent_in_locale and parent_in_locale.slug:
        parent_slug_for_hierarchy = parent_in_locale.slug
    else:
        # Fallback: если переведенного родителя нет или у него нет слага.
        # Это может произойти, если родитель еще не был сохранен или его слаг не был установлен.
        # Попытаемся перевести название родителя, чтобы сгенерировать его часть слага.
        # Также добавим refresh_from_db на случай, если слаг не был загружен.
        if parent_in_locale_base and not parent_in_locale_base.slug:
            parent_in_locale_base.refresh_from_db()  # Попытка обновить из БД
            parent_in_locale = parent_in_locale_base.specific  # Перезагрузить specific
            if parent_in_locale and parent_in_locale.slug:
                parent_slug_for_hierarchy = parent_in_locale.slug
                print(
                    f"[build_slug_from_hierarchy] Refreshed and found slug for parent_in_locale: {parent_slug_for_hierarchy}")

        if not parent_slug_for_hierarchy:  # Если слаг все еще не найден
            try:
                temp_translator = Translator(from_lang=parent.locale.language_code, to_lang=lang)
                translated_parent_title = temp_translator.translate(parent.title)
                parent_slug_for_hierarchy = slugify(unidecode(translated_parent_title.lower()))
                print(
                    f"[build_slug_from_hierarchy] Translated parent slug for hierarchy (fallback): {parent_slug_for_hierarchy} for parent {parent.title} ({parent.locale.language_code}) to {lang}.")
            except Exception as e:
                print(
                    f"[build_slug_from_hierarchy] Warning: Could not get translated parent slug for {parent.title} ({parent.locale.language_code}) to {lang} (fallback to original title slug): {e}")
                parent_slug_for_hierarchy = slugify(
                    unidecode(parent.title.lower()))  # Fallback к оригинальному названию родителя

    # Комбинируем слаг родителя с текущим слагом
    base_slug = f"{parent_slug_for_hierarchy}-{current_slug_part}"
    return ensure_unique_slug(base_slug, instance, locale_obj)


@receiver(pre_save)
def auto_slug_all(sender, instance, **kwargs):
    if not isinstance(instance, Page):
        return
    if getattr(instance, '_processing', False):
        return

    lang = instance.locale.language_code.split('-')[0]
    expected_slug_from_title = slugify(unidecode(instance.title.lower()))

    should_regenerate_slug = False

    # 1. Если это новая страница
    if not instance.pk:
        should_regenerate_slug = True
    # 2. Если слаг пуст
    elif not instance.slug:
        should_regenerate_slug = True
    # 3. Если слаг содержит кириллицу
    elif any(c in instance.slug for c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'):
        should_regenerate_slug = True
    # 4. Для нерусских локалей: если текущий слаг не соответствует сгенерированному из переведенного заголовка
    # (Эта проверка теперь будет сравнивать с полным иерархическим слагом)
    elif lang != 'ru' and instance.slug != expected_slug_from_title:  # Эта строка останется, но expected_slug_from_title будет плоским, а слаг - иерархическим
        # Если слаг не совпадает с плоским вариантом, но должен быть иерархическим,
        # это условие может быть слишком простым.
        # Лучше явно проверить, что слаг не соответствует тому, что должен быть
        # сгенерирован build_slug_from_hierarchy
        current_expected_full_slug = build_slug_from_hierarchy(instance, lang=lang)
        if instance.slug != current_expected_full_slug:
            should_regenerate_slug = True
    # 5. Если название изменилось (для русской страницы)
    elif lang == 'ru' and instance.pk:  # Только для существующих русских страниц
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.title != instance.title:
                should_regenerate_slug = True
        except sender.DoesNotExist:
            pass

    if should_regenerate_slug:
        slug = build_slug_from_hierarchy(instance, lang=lang)
        instance.slug = slug
        print(f"[auto_slug_all] Generated slug for {instance.title} ({lang}): {slug}")

    # Записываем измененные поля для использования в post_save (auto_translate)
    if instance.pk:  # Если это не новая страница
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            changed_fields_set = set()
            fields_to_check = ['title', 'draft_title', 'seo_title', 'search_description']

            # Добавляем 'description', если модель имеет это поле
            if hasattr(instance, 'description') and instance._meta.get_field('description').editable:
                fields_to_check.append('description')

            # Добавляем 'topic' для HomePage
            if isinstance(instance, HomePage):
                fields_to_check.append('topic')

            # Добавляем 'image', если оно есть и это не HomePage (у HomePage нет image)
            if hasattr(instance, 'image') and not isinstance(instance, HomePage) and instance._meta.get_field(
                    'image').editable:
                fields_to_check.append('image')

            for field_name in fields_to_check:
                old_value = getattr(old_instance, field_name, None)
                new_value = getattr(instance, field_name, None)

                # Специальная обработка для полей типа Image (ForeignKey)
                if field_name == 'image' and hasattr(old_instance, 'image') and hasattr(instance, 'image'):
                    if old_instance.image_id != instance.image_id:
                        changed_fields_set.add(field_name)
                elif old_value != new_value:
                    changed_fields_set.add(field_name)

            # Добавляем slug и url_path, если они изменились
            if old_instance.slug != instance.slug:
                changed_fields_set.add('slug')
            if old_instance.url_path != instance.url_path:
                changed_fields_set.add('url_path')

            instance._changed_fields_on_save = list(changed_fields_set)
        except sender.DoesNotExist:
            instance._changed_fields_on_save = []
    else:  # Новая страница, все поля считаем измененными
        # Определяем список полей, которые есть у данного типа страницы
        new_page_fields = ['title', 'draft_title', 'seo_title', 'search_description']
        if isinstance(instance, (Product, Recipe)):
            new_page_fields.append('description')
        if isinstance(instance, HomePage):
            new_page_fields.append('topic')
        if hasattr(instance, 'image') and not isinstance(instance, HomePage):
            new_page_fields.append('image')
        new_page_fields.append('slug')
        instance._changed_fields_on_save = new_page_fields


def _translate_richtext(text, translator):
    if not text:
        return text

    soup = BeautifulSoup(expand_db_html(text), 'html.parser')
    for element in soup.find_all(string=True):
        if not isinstance(element, NavigableString):
            continue
        if element.parent.name in ['script', 'style']:
            continue
        original_text = str(element).strip()
        if original_text:
            try:
                translated_text = translator.translate(original_text)
                element.replace_with(translated_text)
            except Exception as e:
                print(f"Error translating RichText part '{original_text}': {e}")
    return str(soup)


@receiver(post_save)
def auto_translate(sender, instance, created, **kwargs):
    if not isinstance(instance, (Category, Product, Recipe, HomePage)):  # Убедитесь, что все ваши модели здесь
        return

    if getattr(_auto_translate_processing_lock, 'active', False):
        print(f"[auto_translate] Skipping {instance.title} (id={instance.id}) due to active lock.")
        return

    _auto_translate_processing_lock.active = True

    try:
        if instance.locale.language_code != 'ru':
            print(f"[auto_translate] Skipping {instance.title} (id={instance.id}): not Russian locale.")
            return

        if getattr(instance, '_processing', False):
            print(f"[auto_translate] Skipping {instance.title} (id={instance.id}) due to _processing flag.")
            return

        print(
            f"[auto_translate] Processing: {instance.title} (ru, id={instance.id}, depth={instance.depth}, path={instance.path})")

        # Используем _changed_fields_on_save, установленный в pre_save
        changed_fields = getattr(instance, '_changed_fields_on_save', [])

        # Если страница только что создана, changed_fields уже установлен в pre_save
        if created:
            print(
                f"[auto_translate] Instance created. All relevant fields considered changed for {instance.title} (id={instance.id}).")

        print(f"[auto_translate] Changed fields for {instance.title} (id={instance.id}): {changed_fields}")
        if not changed_fields:
            print(
                f"[auto_translate] No relevant fields changed for {instance.title} (id={instance.id}): {changed_fields}")
            return  # Если ничего не изменилось, выходим

        parent = instance.get_parent()
        print(
            f"[auto_translate] Parent: {parent.title} (id={parent.id}, depth={parent.depth}, path={parent.path})" if parent else "[auto_translate] No parent for instance.")

        target_locales = ['en', 'sr']

        for code in target_locales:
            print(f"[auto_translate] Processing locale: {code}")
            locale = Locale.objects.get(language_code=code)
            translator = Translator(from_lang='ru', to_lang=code)

            translated_title = translator.translate(instance.title)
            print(f"[auto_translate] Translated title for {code}: {translated_title}")

            parent_in_locale = None
            if parent:
                parent_in_locale_base = Page.objects.filter(
                    translation_key=parent.translation_key, locale=locale
                ).first()

                if parent_in_locale_base:
                    parent_in_locale = parent_in_locale_base.specific
                else:
                    print(f"[auto_translate] Creating {code} parent for: {parent.title}")
                    # Создаем экземпляр родительского класса
                    parent_in_locale = parent.__class__(
                        title=translator.translate(parent.title),
                        slug=build_slug_from_hierarchy(parent, lang=code),
                        # Слаг родителя тоже должен быть иерархическим
                        locale=locale,
                        translation_key=parent.translation_key,
                        draft_title=translator.translate(parent.draft_title) if parent.draft_title else '',
                        seo_title=translator.translate(parent.seo_title) if parent.seo_title else '',
                        search_description=translator.translate(
                            parent.search_description) if parent.search_description else '',
                    )
                    grandparent = parent.get_parent()
                    grandparent_in_locale = None
                    if grandparent:
                        grandparent_in_locale_base = Page.objects.filter(
                            translation_key=grandparent.translation_key, locale=locale
                        ).first()
                        if grandparent_in_locale_base:
                            grandparent_in_locale = grandparent_in_locale_base.specific

                    if not grandparent_in_locale:
                        print(
                            f"[auto_translate] ERROR: Grandparent for {parent.title} ({code}) not found. Translation might fail.")
                        continue

                    with translation.override(code):
                        grandparent_in_locale._processing = True
                        parent_in_locale._processing = True
                        grandparent_in_locale.add_child(instance=parent_in_locale)
                        parent_in_locale.save()
                        parent_in_locale.save_revision().publish()
                        parent_in_locale._processing = False
                        grandparent_in_locale._processing = False
                    print(
                        f"[auto_translate] Created {code} parent: {parent_in_locale.title} (id={parent_in_locale.id})")

                if parent_in_locale:
                    print(
                        f"[auto_translate] Found parent for {code}: {parent_in_locale.title} (id={parent_in_locale.id}, depth={parent_in_locale.depth}, path={parent_in_locale.path})")
                    parent_changed = False
                    parent_fields_to_check = ['title', 'draft_title', 'seo_title', 'search_description']
                    for field_name in parent_fields_to_check:
                        original_parent_value = getattr(parent, field_name, None)
                        if original_parent_value:
                            translated_parent_value = translator.translate(original_parent_value)
                            if getattr(parent_in_locale, field_name) != translated_parent_value:
                                setattr(parent_in_locale, field_name, translated_parent_value)
                                parent_changed = True
                    # Также обновить слаг родителя, если он должен измениться
                    expected_parent_slug = build_slug_from_hierarchy(parent_in_locale, lang=code)
                    if parent_in_locale.slug != expected_parent_slug:
                        parent_in_locale.slug = expected_parent_slug
                        parent_changed = True

                    if parent_changed:
                        with translation.override(code):
                            parent_in_locale._processing = True
                            parent_in_locale.save()
                            parent_in_locale.save_revision().publish()
                            parent_in_locale._processing = False
                        print(f"[auto_translate] Updated {code} parent: {parent_in_locale.title}")

            target_base = Page.objects.filter(
                translation_key=instance.translation_key, locale=locale
            ).first()

            target = target_base.specific if target_base else None

            # Определяем, какие поля нужно переводить на основе changed_fields
            fields_to_translate = {}
            source_fields = {
                'title': instance.title,
                'draft_title': instance.draft_title,
                'seo_title': instance.seo_title,
                'search_description': instance.search_description,
                'description': getattr(instance, 'description', None) if hasattr(instance, 'description') else None,
                'topic': instance.topic if isinstance(instance, HomePage) else None,
                'image': instance.image if hasattr(instance, 'image') and not isinstance(instance, HomePage) else None,
            }

            for field_name, original_value in source_fields.items():
                # Переводим поле, только если оно было изменено (или если это создание страницы)
                if created or field_name in changed_fields:
                    if original_value is not None:  # Проверяем, что значение не None перед переводом
                        if isinstance(sender._meta.get_field(field_name), RichTextField):
                            translated_data_value = _translate_richtext(original_value, translator)
                        elif isinstance(sender._meta.get_field(field_name), (CharField, TextField)):
                            translated_data_value = translator.translate(original_value)
                        elif field_name == 'image':
                            # Для изображений, мы не переводим само изображение, а просто копируем ссылку
                            translated_data_value = original_value
                        else:
                            translated_data_value = original_value
                    else:  # Если original_value is None, просто передаем None
                        translated_data_value = None

                    fields_to_translate[field_name] = translated_data_value
                elif target:  # Если поле не изменилось, но страница уже существует, сохраняем ее текущее значение
                    fields_to_translate[field_name] = getattr(target, field_name, None)
                else:  # Если поле не изменилось и это создание новой страницы, оставляем как есть (скорее всего None)
                    fields_to_translate[field_name] = original_value

            if target:
                updated = False
                for field_name, translated_value in fields_to_translate.items():
                    # Специальная обработка для image: сравниваем image_id
                    if field_name == 'image' and hasattr(target, 'image') and hasattr(translated_value,
                                                                                      'id'):  # translated_value может быть Image
                        if target.image_id != translated_value.id:
                            setattr(target, field_name, translated_value)
                            updated = True
                    # Если translated_value - None, а target.image_id - не None, то изображение удалено
                    elif field_name == 'image' and hasattr(target,
                                                           'image') and translated_value is None and target.image_id is not None:
                        setattr(target, field_name, None)
                        updated = True
                    elif getattr(target, field_name, None) != translated_value:
                        setattr(target, field_name, translated_value)
                        updated = True

                # Также обновляем слаг, если он должен измениться
                expected_target_slug = build_slug_from_hierarchy(target, lang=code)
                if target.slug != expected_target_slug:
                    target.slug = expected_target_slug
                    updated = True

                if updated:
                    with translation.override(code):
                        target._processing = True
                        target.save()
                        target.save_revision().publish()
                        target._processing = False
                    print(f"[auto_translate] Updated {code} translation: {target.title}")
                else:
                    print(f"[auto_translate] No changes for {code} translation: {target.title}")
            else:
                # Создаем новый перевод
                new_target_args = {
                    'title': fields_to_translate.get('title'),
                    'locale': locale,
                    'translation_key': instance.translation_key,
                    'draft_title': fields_to_translate.get('draft_title'),
                    'seo_title': fields_to_translate.get('seo_title'),
                    'search_description': fields_to_translate.get('search_description'),
                }

                if hasattr(instance, 'description') and instance._meta.get_field(
                        'description').editable:
                    new_target_args['description'] = fields_to_translate.get('description')
                if isinstance(instance, HomePage):
                    new_target_args['topic'] = fields_to_translate.get('topic')
                if hasattr(instance, 'image') and not isinstance(instance,
                                                                 HomePage):
                    new_target_args['image'] = fields_to_translate.get('image')

                new_target = instance.__class__(**new_target_args)

                # Пересчитываем слаг для новой страницы, используя иерархию переведенных родителей
                new_target.slug = build_slug_from_hierarchy(new_target, lang=code)

                if parent_in_locale:
                    with translation.override(code):
                        new_target._processing = True
                        parent_in_locale.add_child(instance=new_target)
                        new_target.save()
                        new_target.save_revision().publish()
                        new_target._processing = False
                    print(f"[auto_translate] Created {code} translation: {new_target.title} (id={new_target.id})")
                else:
                    print(
                        f"[auto_translate] ERROR: Cannot create {code} translation for {instance.title}. Parent not found in locale.")

    except Exception as e:
        print(f"[auto_translate] Critical error processing {instance.title} (id={instance.id}): {e}")
        # raise # Закомментируйте 'raise' для отладки, чтобы ошибки не останавливали весь процесс.
    finally:
        _auto_translate_processing_lock.active = False