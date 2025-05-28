from wagtail.models import Page

# посмотреть всё дерево страниц с заголовками, слагами и урлами
def print_tree(page, level=0):
    print(level, "  " * level + f"- {page.title} | slug: {page.slug} | url: {page.url if hasattr(page, 'url') else page.get_url()}")
    for child in page.get_children().specific():
        print_tree(child, level + 1)
        if level == 4:
            break

root = Page.get_first_root_node()
print_tree(root)


# Добавить страницы в меню
for page in Page.objects.all():
    if not page.show_in_menus:
        page.show_in_menus = True
        page.save()


# Чтобы опубликовать все страницы, которые ещё не опубликованы (live=False):
for page in Page.objects.filter(live=False):
    # Для Wagtail 2.x и 3.x
    if hasattr(page, 'save_revision'):
        page.save_revision().publish()