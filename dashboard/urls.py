from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/dashboard.html'), name='dashboard'),
    path('ai-intro/', TemplateView.as_view(template_name='dashboard/ai_intro.html'), name='ai_intro'),

]