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
    path('<int:user_id>/personal-details/', views.pers_details, name='pers-details')
]

# hotel-related
urlpatterns += [
    path('hotels/', views.hotels, name='anon_hotels'),
    path('<int:user_id>/hotels/', views.hotels, name='hotels'),
    path('hotels/<int:hotel_id>/', views.hotel_details, name='anon_hotel-details'),
    path('<int:user_id>/hotels/<int:hotel_id>/', views.hotel_details, name='hotel-details'),
    path('hotels/<int:hotel_id>/signup/', views.signup, name='hotel-signup-redirect'),
    path('hotels/<int:hotel_id>/signin/', views.signin, name='hotel-signin-redirect'),
    path('<int:user_id>/submit-review/<int:hotel_id>/', views.review, name='review')
]

# checkout
urlpatterns += [
    path('<int:user_id>/checkout/<int:hotel_id>', views.checkout, name='checkout'),
    path('<int:user_id>/pay-suc/', views.pay_suc, name='pay-suc')
]