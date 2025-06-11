from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('infopage.urls')),
    path('adminapp/', include ('adminapp.urls')),
    path('brunhildaapp/', include ('brunhildaapp.urls')),
    path('pepaapp/', include ('pepaapp.urls')),
    path('karelapp/', include ('karelapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
