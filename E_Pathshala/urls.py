
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
import accounts.views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',accounts.views.home,name='home'),
    path('accounts/',include('accounts.urls')),
    path('courses/',include('courses.urls')),
    path('forum/',include('forum.urls')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

