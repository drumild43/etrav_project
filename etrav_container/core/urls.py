from django.urls import path

from . import views

app_name = 'core'

# home + auth
urlpatterns = [
    path('', views.home, name='anon_homepage'),
    path('<int:user_id>/', views.home, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('<int:user_id>/logout/', views.logout, name='logout')   
]

# profile
urlpatterns += [
    path('<int:user_id>/account/', views.account, name='account'),
    path('<int:user_id>/can-booking/<int:booking_id>/', views.cancel_booking, name='cancel-booking'),
]