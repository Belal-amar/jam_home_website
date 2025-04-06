from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name="home"),
    path('login',views.login,name="login"),
    path('register',views.register,name="register"),
    path('categories',views.categories,name="categories"),
    path('category/<int:category_id>/', views.category_products, name="category_products"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),  # Ensure 'cart' URL pattern exists
     path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('location/', views.location, name='location'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('logout/', views.logout, name='logout'),
]