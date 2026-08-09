from django.contrib import admin
from django.urls import path, include
from ish_hub import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('jobs/', include('jobs.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('applications/', include('applications.urls')),

    path("api/", include("ish_hub.api_urls")),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)