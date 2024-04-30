"""
URL configuration for E_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from UserApp import views as user_views
from SellerApp import views as seller_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',user_views.home,name='home'),
    path('about_us/',user_views.about_us,name='about_us'),
    path('contact_us/',user_views.contact,name='contact'),
    path('store_locations/',user_views.store_locations,name='store'),
    path('home/category/<int:cat_id>/',user_views.category_function,name='category'),
    path('product_details/<int:pro_id>',user_views.product_details,name='product_details'),
    path('login/',user_views.login,name='login'),
    path('sign_up/',user_views.sign_up,name='sign_up'),
    path('home/dashboard',user_views.dashboard,name='dashboard'),
    path('home/cart',user_views.cart,name='cart'),
    path('home/cart/remove-cart/<int:cart_id>',user_views.cart_remove,name='remove-cart'),
    path('home/cart/save-cart/<int:cart_id>',user_views.cart_save,name='save-later'),
    path('home/my_account',user_views.my_account,name='my_account'),
    path('home/my_address',user_views.my_address,name='my_address'),
    path('home/my_account/change_password',user_views.change_password,name='change_password'),
    path('home/my_address/delete-address/<int:add_id>',user_views.delete_address,name='delete-address'),
    path('home/my_orders',user_views.my_orders,name='my_orders'),
    path('home/payments',user_views.my_payments,name='my_payments'),
    path('home/my_account/wishlist',user_views.my_wishlist,name='my_wishlist'),
    path('home/my_account/wishlist/remove-wish/<int:wish_id>',user_views.remove_wishlist,name='remove_wish'),
    path('search_results/',user_views.search_results,name='search_results'),
    path('purchase_product/<int:product_id>',user_views.purchase_product,name='buy_now'),

    path('logout/',user_views.logout,name='logout'),
    path('deactivate/<int:user_id>',user_views.deactivate,name='deactivate'),
    path('seller_home/',seller_views.home,name='seller_home'),
    path('seller_home/account_details/',seller_views.account_details,name='seller_details'),
    path('seller_home/my_listing/',seller_views.my_listing,name='my_listing'),
    path('seller_home/add_listing/',seller_views.add_listing,name='add_listing'),
    path('seller_home/add_discount/',seller_views.add_discount,name='add_discount'),
    path('seller_home/active_orders/',seller_views.active_orders,name='active_orders'),
    path('seller_registration/',seller_views.seller_registration,name='seller_registration'),
    path('seller_login/',seller_views.seller_login,name='seller_login'),
    path('seller_logout/',seller_views.seller_logout,name='seller_logout'),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paypal-reverse/',user_views.paypal_reverse,name='paypal_reverse'),
    path('paypal_cancel/',user_views.paypal_cancel,name='paypal_cancel'),






] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
