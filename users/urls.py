from django.urls import path, include
from django.contrib.auth import views as auth_views

from users.views import custom_logout_view


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),

]
