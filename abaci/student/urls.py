from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('submit/<class_id>', views.vote, name='student-vote'),
    path('', views.home, name='student-home'),
    path('info/', TemplateView.as_view(template_name='student/info.html'),name='info'),
]