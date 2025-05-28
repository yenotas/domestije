from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.utils.translation import activate, get_language
from wagtail.models import Locale, Page

from domestije_rs.settings import base
from .models import Category, HomePage


class LocaleHomePageView(TemplateView):
    template_name = "home/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get('locale', 'en')
        locale = Locale.objects.filter(language_code=lang).first()
        if not locale:
            raise Http404(f"Locale {lang} not found")
        home = HomePage.objects.filter(locale=locale, depth=3).first()
        if not home:
            raise Http404(f"HomePage for locale {lang} not found")
        categories = Category.objects.live().descendant_of(home).filter(depth=4)
        print(
            f"[LocaleHomePageView] Locale: {lang}, Home: {home.title}, Slug: {home.slug}, Path: {home.path}, Categories: {list(categories.values('title', 'depth', 'path'))}")
        context["categories"] = categories
        context["current_lang"] = lang
        context["LANGUAGES"] = base.LANGUAGES
        return context


def category_view(request, locale, path):
    """
    Обрабатывает страницы категорий и продуктов: /<locale>/<slug>/
    """
    locale_obj = Locale.objects.filter(language_code=locale).first()
    if not locale_obj:
        raise Http404(f"Locale {locale} not found")
    # Используем последний сегмент пути как слаг
    slug = path.strip('/').split('/')[-1]
    # Ищем страницу (Category или Product) по слагу и локали
    page = Page.objects.filter(locale=locale_obj, slug=slug).live().specific().first()
    if not page:
        raise Http404(f"Page with slug {slug} not found in locale {locale}")
    # Формируем ожидаемый URL через page.get_url
    expected_url = page.get_url(request)
    current_url = f"/{locale}/{path}/"
    if current_url != expected_url:
        # Перенаправляем на корректный URL
        return redirect(expected_url)
    print(f"[category_view] Locale: {locale}, Page: {page.title}, Slug: {slug}, Path: {path}, URL: {expected_url}")
    return page.serve(request)


def set_language(request):
    """
    Переключает язык через GET-параметр.
    """
    lang = request.GET.get('lang', 'en')
    activate(lang)
    response = HttpResponseRedirect('/')
    response.set_cookie('preferred_lang', lang, max_age=31536000)
    return response


def category_tree(request):
    """
    Возвращает дерево категорий (AJAX или шаблон).
    """
    lang = request.GET.get("lang") or get_language('en')
    locale = Locale.objects.filter(language_code=lang).first()
    if not locale:
        locale = Locale.objects.get(language_code='en')

    categories = Category.objects.filter(depth=4, locale=locale).live()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render(request, 'home/categories_list.html', {'categories': categories}).content.decode('utf-8')
        return JsonResponse({'html': html})

    return render(request, 'home/home_page.html', {
        'categories': categories,
        'current_lang': lang
    })