from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', views.u_register, name='register'),
    path('login/', views.u_login, name='login'),
    #path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('about/', views.about, name='about'),
]
