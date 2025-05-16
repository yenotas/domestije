from django.db import models
import json

from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from django.conf import settings
from django.db import models
from modeltranslation.translator import TranslationOptions, register


class HomePage(Page):
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    topic = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('topic'),
    ]


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


# Мультиязычность через django-modeltranslation
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=64, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name='products')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
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

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

class Slider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    link_type = models.CharField(
        max_length=20,
        choices=[('product', 'Товар'), ('category', 'Категория'), ('external', 'Внешняя ссылка')]
    )
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    external_url = models.URLField(blank=True)

@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle',)

class Promotion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='promotions', blank=True)
    categories = models.ManyToManyField(Category, related_name='promotions', blank=True)