from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from search import views as search_views

# 🟢 Кастомные вьюшки
from home.views import category_tree, set_language, LocaleHomePageView, category_view

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("admin/", include(wagtailadmin_urls)),
    path("set-language/", set_language, name="set_language"),
    path("categories/ajax/", category_tree, name="ajax_category_tree"),
    path('<str:locale>/', LocaleHomePageView.as_view(), name='home'),
    path('<str:locale>/<path:path>/', category_view, name='category'),
    re_path(r'^', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

