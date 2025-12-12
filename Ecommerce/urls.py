"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app1.views import home,Category,ProfileView,Product_Details,About,Sign_Up,Login,Logout,update_address,delete_address,add_to_cart,show_Cart,plus_cart,minus_cart,remove_cart,Checkout,paymenthandler,wishlist_view,minus_wishlist,plus_wishlist,View_all,Search,Orders,contact

urlpatterns = [

    ##### Login #########
    path('signup',Sign_Up, name='signup'),
    path('login',Login,name='login'),
    path('ourproducts',View_all,name='ourproducts'),
    path('logout',Logout, name='logout'),
    path('profile',ProfileView.as_view(),name='profile'),
    path('update_address/<int:pk>/',update_address, name='update_address'),
    path('delete_address/<int:pk>/',delete_address, name='delete_address'),

    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('contact/', contact, name='contact'),
    path('category/<slug:val>',Category.as_view(),name='category'),
    path('product_details/<int:pk>',Product_Details.as_view(),name='product_details'),
    path('about',About,name='about'),
    path('addtocart',add_to_cart, name='addtocart'),
    path('cart',show_Cart, name='cart'),
    path('pluscart',plus_cart),
    path('minuscart',minus_cart),
    path('removecart',remove_cart, name='removecart'),

    path('wishlist/', wishlist_view, name='wishlist'),
    path('pluswishlist/', plus_wishlist),
    path('minuswishlist/', minus_wishlist),



    path('checkout',Checkout.as_view(),name='checkout'),
    path('paymenthandler/',paymenthandler, name='paymenthandler'),
    path('orders',Orders,name ='orders'),

    path('search',Search, name='search')
    

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Melody Mart"
admin.site.site_title = "Melody Mart"

admin.site.site_index_title = "Welcome To Melody Mart"
