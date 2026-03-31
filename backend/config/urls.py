from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.authentication.urls")),
    path("api/chat/", include("apps.chatbot.urls")),
    path("api/documents/", include("apps.documents.urls")),
    path("api/admin/", include("apps.admin_dashboard.urls")),
    path("api/users/", include("apps.users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
