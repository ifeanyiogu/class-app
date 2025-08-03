from django.urls import path
from .views import LoginView, RegisterUserView, LogoutView, HomeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("", HomeView.as_view()),
]