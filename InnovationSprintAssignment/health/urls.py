from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/',views.register,name='register'),
    path('add_temperature/',views.AddTempCreateView.as_view(),name='add_temperature'),
    path('profile/',views.profile,name='profile')

]