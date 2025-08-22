from django.urls import path
from . import views

urlpatterns = [
    path('all/<int:pk>/', views.AllComments.as_view()),
    path('one/<int:pk>/', views.OneComment.as_view()),
    path('create/<int:pk>/', views.CreateComment.as_view()),
    path('reply/<int:pk>/', views.AllReplies.as_view()),
    path('reply-create/<int:pk>/', views.CreateReply.as_view())
]