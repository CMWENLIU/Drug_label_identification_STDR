from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from uploads.core import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^uploads/simple/$', views.simple_upload, name='simple_upload'),
    url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^admin/', admin.site.urls),
    url(r'^/recognize/', views.recognize, name='recognize'),
    url(r'^/yop/', views.top, name='top')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
