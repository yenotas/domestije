import os
import sys
import re
import django
from django.utils.text import slugify
from unidecode import unidecode


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domestije_rs.settings.dev')
django.setup()
# <-- ВСЕ ИМПОРТЫ ПОСЛЕ setup()
from wagtail.models import Locale
from home.models import HomePage, Category
# from home.tools.tools_lib import SUFFIXES_PRODUCTS, generate_suffixed_slug

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

files = {
    'ru': os.path.join(SCRIPT_DIR, 'tools/struct_ru.txt'),
    'sr': os.path.join(SCRIPT_DIR, 'tools/struct_sr.txt'),
    'en': os.path.join(SCRIPT_DIR, 'tools/struct_en.txt'),
}


def parse_file(filename):
    with open(filename, encoding='utf-8-sig') as f:
        return [line.strip() for line in f if line.strip()]


def parse_structures():
    lines = {lang: parse_file(path) for lang, path in files.items()}
    line_count = len(lines['ru'])
    assert all(len(lines[lang]) == line_count for lang in lines), "Файлы имеют разное число строк!"

    categories = []
    stack = []

    for i in range(line_count):
        m_ru = re.match(r"^([\d.]+)\s+(.+)$", lines['ru'][i])
        m_sr = re.match(r"^([\d.]+)\s+(.+)$", lines['sr'][i])
        m_en = re.match(r"^([\d.]+)\s+(.+)$", lines['en'][i])
        if not (m_ru and m_sr and m_en):
            print(f"Пропуск строки {i+1}: некорректный формат")
            continue
        num = m_ru.group(1).rstrip('.')
        level = num.count('.') + 1
        title_ru = m_ru.group(2)
        title_sr = m_sr.group(2)
        title_en = m_en.group(2)

        category = {
            'num': num,
            'level': level,
            'title_ru': title_ru,
            'title_sr': title_sr,
            'title_en': title_en,
            'children': [],
            'parent': None,
        }

        if level == 1:
            categories.append(category)
            stack = [category]
        else:
            while stack and stack[-1]['level'] >= level:
                stack.pop()
            if stack:
                category['parent'] = stack[-1]
                stack[-1]['children'].append(category)
            stack.append(category)
    return categories


def save_categories(categories, parent_ru=None, parent_translations=None,
                    slug_path_ru=None, slug_paths_trans=None):

    if parent_translations is None:
        parent_translations = {}
    if slug_path_ru is None:
        slug_path_ru = []
    if slug_paths_trans is None:
        slug_paths_trans = {'en': [], 'sr': []}

    ru_locale = Locale.objects.get(language_code='ru')
    en_locale = Locale.objects.get(language_code='en')
    sr_locale = Locale.objects.get(language_code='sr')

    home_ru = HomePage.objects.get(title__iexact='ru')
    home_en = HomePage.objects.get(title__iexact='en')
    home_sr = HomePage.objects.get(title__iexact='sr')

    for cat in categories:
        # Добавляем название к текущему пути
        new_slug_path_ru = slug_path_ru + [cat['title_ru']]
        new_slug_paths_trans = {
            'en': slug_paths_trans['en'] + [cat['title_en']],
            'sr': slug_paths_trans['sr'] + [cat['title_sr']],
        }

        # --- категория на русском ---
        slug_ru = slugify(unidecode("-".join(new_slug_path_ru)))
        db_cat = Category(
            title=cat['title_ru'],
            slug=slug_ru,
            locale=ru_locale,
        )

        print(f"Русские категории > title = {cat['title_ru']},  slug = {slug_ru}")

        if parent_ru:
            parent_ru.add_child(instance=db_cat)
        else:
            home_ru.add_child(instance=db_cat)

        db_cat.save_revision().publish()

        # --- переводы ---
        translations = {'ru': db_cat}
        for code, locale, title, home in [
            ('en', en_locale, cat['title_en'], home_en),
            ('sr', sr_locale, cat['title_sr'], home_sr)
        ]:
            parent_trans = parent_translations.get(code)
            slug_parts = new_slug_paths_trans[code]
            slug = slugify(unidecode("-".join(slug_parts)))

            if parent_trans:
                translated = db_cat.copy_for_translation(locale=locale, copy_parents=False)
                translated.title = title
                translated.slug = slug
                translated.save_revision().publish()
                translated.move(parent_trans, pos='last-child')
            else:
                # РОДИТЕЛЬ НЕ ПЕРЕВЕДЁН: создаём перевод вручную
                translated = Category(
                    title=title,
                    slug=slug,
                    locale=locale,
                    translation_key=db_cat.translation_key,
                )
                home.add_child(instance=translated)
                translated.save_revision().publish()

            print(f"title = {title},  slug = {slug}")
            translations[code] = translated

        # --- рекурсивный вызов ---
        save_categories(
            cat['children'],
            parent_ru=db_cat,
            parent_translations=translations,
            slug_path_ru=new_slug_path_ru,
            slug_paths_trans=new_slug_paths_trans
        )


def main():
    categories = parse_structures()
    save_categories(categories)


if __name__ == "__main__":
    main()
