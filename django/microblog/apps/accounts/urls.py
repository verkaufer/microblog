from django.urls import path

from accounts.api.views import (LoginView, LogoutView, ProfileView, RegisterView, FollowUserView)

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profiles/<str:username>/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('follows/', FollowUserView.as_view(), name='follows')
]