
from django.contrib import admin
from django.urls import path , include 
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='landing'),
    path('api/face/', include('authapp.urls')),
    path('dashboard/', include('dashboard.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)