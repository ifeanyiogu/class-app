from django.urls import path
from . import views

urlpatterns = [
    path('list/<int:pk>/', views.ListAssignments.as_view()),
    path('one/<int:pk>/', views.OneAssignment.as_view()),
    path('create/<int:pk>/', views.CreateAssignment.as_view()),
    path('up-del/<int:pk>/', views.UpdateDeleteAssignment.as_view())
]