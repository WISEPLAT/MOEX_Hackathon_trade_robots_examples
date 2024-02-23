
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('name.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
