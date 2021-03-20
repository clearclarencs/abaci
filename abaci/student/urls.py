from django.urls import path
from . import views
from django.views.generic import TemplateView
'''STUDENT APP, URLS, define the page urls'''
urlpatterns = [
    # Class id in url so can bookmark url
    path('submit/<class_id>', views.vote, name='student-vote'),
    # Home page is student login
    path('', views.home, name='student-home'),
    # Simple info page of html
    path('info/', TemplateView.as_view(template_name='student/info.html'),name='info'),
]