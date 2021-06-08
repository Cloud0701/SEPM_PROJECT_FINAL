from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('',views.homepage,name="homepage"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('loginpage/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('registrationpage/',views.register,name='register'),
	path('update_item/', views.updateItem, name="update_item"),
	path('payment/', views.payment,name='payment'),
	path('process_order/', views.processOrder, name="process_order"),
	path('accountpage/',views.accountpage,name="account"),

]