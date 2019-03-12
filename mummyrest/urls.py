from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls.conf import path


PREFIX_API = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
