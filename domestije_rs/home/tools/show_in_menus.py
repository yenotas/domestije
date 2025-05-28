import django
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domestije_rs.settings.dev')
django.setup()
from home.models import Category

def enable_show_in_menus():
    count = 0
    for cat in Category.objects.all():
        if not cat.show_in_menus:
            cat.show_in_menus = True
            cat.save()
            count += 1
    print(f"✅ Обновлено {count} категорий")

# Запускать в Django shell
enable_show_in_menus()
