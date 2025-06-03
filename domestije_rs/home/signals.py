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
    elif lang != 'ru' and instance.slug != expected_slug_from_title:
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
            if isinstance(instance, (Product, Recipe)):
                fields_to_check.append('description')
            if isinstance(instance, HomePage):
                fields_to_check.append('topic')
            # Добавляем image, если оно есть и это не HomePage (у HomePage нет image)
            if hasattr(instance, 'image') and not isinstance(instance, HomePage):
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
                        slug=slugify(unidecode(translator.translate(parent.title).lower())),
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
                'description': instance.description if isinstance(instance, (Product, Recipe)) else None,
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
                    # 'slug': slugify(unidecode(fields_to_translate.get('title', '').lower())),
                    'locale': locale,
                    'translation_key': instance.translation_key,
                    'draft_title': fields_to_translate.get('draft_title'),
                    'seo_title': fields_to_translate.get('seo_title'),
                    'search_description': fields_to_translate.get('search_description'),
                }

                if isinstance(instance, (Product, Recipe)):
                    new_target_args['description'] = fields_to_translate.get('description')
                if isinstance(instance, HomePage):
                    new_target_args['topic'] = fields_to_translate.get('topic')
                if hasattr(instance, 'image') and not isinstance(instance,
                                                                 HomePage):  # image есть и не HomePage
                    new_target_args['image'] = fields_to_translate.get('image')

                new_target = instance.__class__(**new_target_args)

                # Пересчитываем слаг для новой страницы, используя иерархию переведенных родителей
                # new_target.slug = build_slug_from_hierarchy(new_target, lang=code)

                if parent_in_locale:
                    with translation.override(code):
                        new_target._processing = True
                        parent_in_locale.add_child(instance=new_target)  # <-- Здесь происходит первый pre_save, который вызывает auto_slug_all
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


def build_slug_from_hierarchy(instance, lang=None):
    locale_obj = Locale.objects.get(language_code=lang) if lang else instance.locale
    current_slug_part = slugify(unidecode(instance.title.lower()))

    # Определяем глубину для логики формирования слага
    calculated_depth = instance.depth
    parent = instance.get_parent()  # Получаем родителя здесь

    if calculated_depth is None:
        if parent:
            # Если у родителя нет глубины (что тоже странно), то предполагаем
            # что родитель на 3 уровне, а текущий на 4.
            calculated_depth = parent.depth + 1 if parent.depth is not None else 4
        else:
            # Если нет родителя и depth равен None
            if isinstance(instance, HomePage):
                calculated_depth = 3
            else:
                calculated_depth = 4  # Для корневых категорий под Home
            print(
                f"[build_slug_from_hierarchy] Warning: instance.depth is None and no parent for {instance.title}. "
                f"Inferring depth {calculated_depth} based on page type (for slug logic).")

    # Логика формирования слага в зависимости от рассчитанной глубины
    if calculated_depth < 5:
        # Для depth < 5 — плоский слаг (только текущая часть)
        return ensure_unique_slug(current_slug_part, instance, locale_obj)
    else:
        # Для depth >= 5 — склеенный слаг (слаг родителя + текущая часть)
        if not parent:
            print(
                f"[build_slug_from_hierarchy] Warning: Page {instance.title} has calculated_depth={calculated_depth} "
                f"but no parent found for hierarchical slug. Falling back to flat slug.")
            return ensure_unique_slug(current_slug_part, instance, locale_obj)  # Fallback to flat slug if no parent

        # Получаем локализованного родителя для его слага
        # Здесь критично, чтобы parent_in_locale имел корректный слаг.
        # Если parent_in_locale только что был создан, его слаг должен был
        # быть установлен auto_slug_all на его pre_save.
        parent_in_locale_base = Page.objects.filter(
            translation_key=parent.translation_key,
            locale=locale_obj
        ).first()

        parent_in_locale = parent_in_locale_base.specific if parent_in_locale_base else None

        parent_slug_for_hierarchy = ""
        if parent_in_locale and parent_in_locale.slug:
            parent_slug_for_hierarchy = parent_in_locale.slug
        else:
            # Если локализованного родителя нет или у него нет слага (что не должно быть после pre_save)
            # или если parent_in_locale - это только что созданный объект,
            # который еще не имеет path/slug из-за transaction-level inconsistency,
            # то это потенциально проблемное место.
            # Для надежности, можно здесь сделать refresh_from_db() для parent_in_locale
            # если он найден, но не имеет слага, или если parent_in_locale_base был найден,
            # но его specific еще не загружен со всеми полями.

            # В данном случае, если parent_in_locale_base существует, но его specific не имеет слага,
            # это может быть проблемой. Однако, обычно Wagtail при загрузке .specific()
            # должен загружать все поля.

            # Попробуем сделать это более надежно, если parent_in_locale не имеет слага
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