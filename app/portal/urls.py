from django.urls import path
from . import views
'''PORTAL APP, URLS, define urls'''
urlpatterns = [
    path('', views.ClssListView.as_view(), name='teacher-portal'), # view classes url
    path('class/<int:pk>/', views.ClssDetailView.as_view(), name='clss-detail'), # view class url
    path('class/<int:pk>/delete/', views.ClssDeleteView.as_view(), name='clss-delete'), # delete class url
    path('class/new/', views.ClssCreateView.as_view(), name='clss-create'), # create class url
    path('topic/<int:pk>/', views.TopicUpdateView.as_view(), name='topic-activate'), # view topic url
    path('topic/<int:pk>/delete', views.TopicDeleteView.as_view(), name='topic-delete'), # delet topic url
    path('class/<int:pk>/new/', views.TopicCreateView.as_view(), name='topic-create'), # create topic url
]