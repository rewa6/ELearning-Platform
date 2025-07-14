from django.urls import path
from .views import RegisterView, LoginView, LogoutView, EndUserLoginView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/enduser-login/', EndUserLoginView.as_view(), name='enduser-login'),
]
