from django.utils.text import slugify
from unidecode import unidecode

SUFFIXES_PRODUCTS = {
    'ru': ['купить', 'заказать', 'купить-или-заказать', 'заказать-или-купить'],
    'en': ['buy', 'order', 'buy-or-order', 'order-or-buy'],
    'sr': ['kupiti', 'poručiti', 'kupiti-ili-poručiti', 'poručiti-ili-kupiti'],
}

SUFFIXES_DEFAULT = {
    'ru': ['черногория', 'сербия', 'черногория-или-сербия', 'сербия-или-черногория'],
    'en': ['montenegro', 'serbia', 'montenegro-or-serbia', 'serbia-or-montenegro'],
    'sr': ['crnagora', 'srbija', 'crnagora-ili-srbija', 'srbija-ili-crnagora'],
}


def generate_suffixed_slug(base_title, parent, suffix_list, Page):
    base = slugify(unidecode(base_title))
    for suffix in suffix_list:
        candidate = f"{base}-{slugify(unidecode(suffix))}"
        if not Page.objects.filter(slug=candidate, path__startswith=parent.path, depth=parent.depth + 1).exists():
            return candidate

    # fallback с цифрой
    i = 2
    while True:
        candidate = f"{base}-{i}"
        if not Page.objects.filter(slug=candidate, path__startswith=parent.path, depth=parent.depth + 1).exists():
            return candidate
        i += 1



def build_slug_from_hierarchy(instance, lang=None):
    """
    Строит slug из названий всех родителей + текущего, используя title на нужном языке
    """
    titles = []
    page = instance
    while page.depth > 3:  # не включаем HomePage (depth=2)
        if lang:
            title = getattr(page.specific, f"title_{lang}", page.title)
        else:
            title = page.title
        titles.insert(0, title)
        page = page.get_parent()

    # добавим текущий title
    if lang:
        titles.append(getattr(instance, f"title_{lang}", instance.title))
    else:
        titles.append(instance.title)

    return slugify(unidecode("-".join(titles)))


