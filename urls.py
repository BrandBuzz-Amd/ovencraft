from django.contrib import admin
from django.urls import path, include
from core import views as core_views  # Add this line
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemap import BlogSitemap
from .admin import admin_site

sitemaps = {
    'blogs': BlogSitemap,
}

urlpatterns = [
    path("admin/", admin_site.urls),
    path("blogs/", include("blog.urls")),
    path("gallery/", include("gallery.urls")),
    path("contact/", include("contact.urls")),
    path("users/", include("users.urls")),

    path("", core_views.index, name="home"),  # root URL
    path("about/", core_views.about, name="about"),  # about URL
    path("products/", core_views.products, name="products"),  # products URL
    path("product-details/", core_views.product_details, name="product-details"),  # product details URL
    path("faq/", core_views.faq, name="faq"),  # added faq URL
    path("privacy-policy/", core_views.privacy_policy, name="privacy-policy"),  # privacy policy URL

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
