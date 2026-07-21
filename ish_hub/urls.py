from django.contrib import admin
from django.urls import path, include
from ish_hub import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('jobs/', include('jobs.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('applications/', include('applications.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

