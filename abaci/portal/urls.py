from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClssListView.as_view(), name='teacher-portal'),
    path('class/<int:pk>/', views.ClssDetailView.as_view(), name='clss-detail'),
    path('class/<int:pk>/delete/', views.ClssDeleteView.as_view(), name='clss-delete'),
    path('class/new/', views.ClssCreateView.as_view(), name='clss-create'),
    path('topic/<int:pk>/', views.TopicUpdateView.as_view(), name='topic-activate'),
    path('topic/<int:pk>/delete', views.TopicDeleteView.as_view(), name='topic-delete'),
    path('class/<int:pk>/new/', views.TopicCreateView.as_view(), name='topic-create'),
]