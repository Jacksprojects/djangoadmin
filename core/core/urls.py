from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from blog.admin import moderator_admin_site, user_admin_site

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls, name='admin'),
    path('mod-admin/', moderator_admin_site.urls, name='mod-admin'),
    path('user-admin/', user_admin_site.urls, name='user-admin'),
) 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)