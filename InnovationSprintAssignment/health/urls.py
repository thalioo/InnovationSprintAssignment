from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/',views.register,name='register'),
    path('add_temperature/',views.AddTempCreateView.as_view(),name='add_temperature'),
    path('profile/',views.profile,name='profile'),
    path('view_temperatures/',views.TemperatureView.as_view(),name='view_temperatures'),
    path('view_active_session/',views.ActiveSessionView.as_view(),name='view_active_session'),
    path('view_sessions_dates/',views.SessionView.as_view(),name ='view_sessions_dates' )

]