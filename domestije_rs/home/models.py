from django.db import models
from django.shortcuts import redirect
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.models import Locale
from django.utils import translation
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from domestije_rs.settings import base


# Главная страница
from django.db import models
from django.shortcuts import redirect
from wagtail.fields import RichTextField
from wagtail.models import Page, Locale
from wagtail.admin.panels import FieldPanel
from django.utils import translation
from domestije_rs.settings import base

from django.db import models
from django.shortcuts import redirect
from wagtail.fields import RichTextField
from wagtail.models import Page, Locale
from wagtail.admin.panels import FieldPanel
from django.utils import translation
from domestije_rs.settings import base

class HomePage(Page):
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    topic = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('topic'),
    ]

    def get_url_parts(self, request=None):
        """
        Формируем URL для HomePage: /<lang>/
        """
        site_root_paths = self._get_site_root_paths(request)
        if not site_root_paths:
            return None
        site_root = site_root_paths[0]
        site_id = site_root.site_id
        root_url = site_root.root_url
        lang = self.locale.language_code
        page_path = f"/{lang}/"
        print(f"[HomePage.get_url_parts] title={self.title}, lang={lang}, path={page_path}")
        return (site_id, root_url, page_path)

    def serve(self, request):
        """
        Язык на основе запроса или cookie.
        """
        requested_lang = request.path.strip('/').split('/')[0] if request.path.strip('/') else ''
        lang = (
            requested_lang or
            request.COOKIES.get('preferred_lang') or
            request.LANGUAGE_CODE or
            self.locale.language_code or
            'en'
        )
        supported_langs = [code for code, _ in base.LANGUAGES]
        if lang not in supported_langs:
            lang = 'en'
        translation.activate(lang)
        response = super().serve(request)
        response.set_cookie('preferred_lang', lang, max_age=31536000)
        return response

    def get_context(self, request):
        context = super().get_context(request)
        lang = request.LANGUAGE_CODE or self.locale.language_code or 'en'
        locale = Locale.objects.filter(language_code=lang).first() or Locale.objects.get(language_code='en')
        home = HomePage.objects.filter(locale=locale, slug=lang, depth=3).first()
        context['categories'] = Category.objects.live().descendant_of(home).filter(depth=4) if home else []
        context['current_lang'] = lang
        context['LANGUAGES'] = base.LANGUAGES
        print(f"[HomePage.get_context] lang={lang}, categories={[cat.title for cat in context['categories']]}")
        return context

class Category(Page):
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0, help_text="Порядок сортировки категории")
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('sort_order'),
        FieldPanel('image'),
    ]

    def get_url_parts(self, request=None):
        """
        Формируем URL: /<lang>/<category_slug>/
        """
        site_root_paths = self._get_site_root_paths(request)
        if not site_root_paths:
            return None
        site_root = site_root_paths[0]
        site_id = site_root.site_id
        root_url = site_root.root_url
        lang = self.locale.language_code
        page_path = f"/{lang}/{self.slug}/"
        print(f"[Category.get_url_parts] title={self.title}, lang={lang}, slug={self.slug}, path={page_path}")
        return (site_id, root_url, page_path)

    def get_context(self, request):
        context = super().get_context(request)
        context['translations'] = {
            page.locale.language_code: page
            for page in self.get_translations().live()
        }
        context['products'] = self.products.live()
        context['LANGUAGES'] = base.LANGUAGES
        context['current_lang'] = request.LANGUAGE_CODE or 'en'
        return context

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['sort_order', 'title']


# Товар
class Product(Page):
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=64, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('sku'),
        FieldPanel('is_active'),
        FieldPanel('categories'),
    ]

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

# Рецепт
class Recipe(Page):
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name='recipes', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('is_active'),
        FieldPanel('categories'),
    ]

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

# Изображения для товара
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

# Заказ
class Order(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=32,
        choices=[
            ('new', 'Новый'),
            ('processing', 'В обработке'),
            ('completed', 'Завершён'),
            ('cancelled', 'Отменён')
        ],
        default='new'
    )

# Позиции в заказе
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

# Слайдер
class Slider(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    link_type = models.CharField(
        max_length=20,
        choices=[('product', 'Товар'), ('category', 'Категория'), ('external', 'Внешняя ссылка')]
    )
    slider_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    slider_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    external_url = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('image'),
        FieldPanel('video_url'),
        FieldPanel('link_type'),
        FieldPanel('slider_category'),
        FieldPanel('slider_product'),
        FieldPanel('external_url'),
    ]

# Акции
class Promotion(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='promotions', blank=True)
    categories = models.ManyToManyField(Category, related_name='promotions', blank=True)

    class Meta:
        verbose_name = "Промоакция"
        verbose_name_plural = "Промоакции"
