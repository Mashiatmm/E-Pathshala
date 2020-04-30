
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import accounts.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',accounts.views.home,name='home'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

