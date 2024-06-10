from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from . import views



#include the urlpatterns
urlpatterns = [
    path('',views.welcome,name='welcome'),#Default-Route-page
    path('login/',views.login,name='login'),#Login-Route-page
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),#class-based logout
    path('signup/',views.signup,name='signup'),#signup-Route
    path('home/',views.home,name='home'),#home-Route
    path('item/<int:pk>/',views.item,name='item'),#item-Route
    path('cart/', views.cart, name='cart'),#cart
    path('add_cart/<int:pk>/add/', views.add_cart, name='add_cart'),#+add to cart
    path('remove_cart/<int:pk>/remove/', views.remove_cart, name='remove_cart'),#-remove from cart
    path('checkout/', views.checkout, name='checkout'),#payment
    path('401/',views.custom_401,name='custom_401'),#unauthorized_rout
]

