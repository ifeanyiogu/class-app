from django.urls import path
from . import views

urlpatterns = [
    path('one/<int:pk>/', views.OneSubmission.as_view()),
    path('all/<int:pk>/', views.AllSubmission.as_view()),
    path('mark/<int:pk>/', views.MarkSubmission.as_view()),
    path('post/<int:pk>/', views.PostSubmission.as_view()), 
]