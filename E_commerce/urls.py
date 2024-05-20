from django.contrib import admin
from UserApp import views as user_views
from SellerApp import views as seller_views
from AdminApp import views as admin_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('admin/',admin_views.dashboard,name='admin_dashboard'),
    path('admin/discount_events',admin_views.discounts,name='admin_discounts'),
    path('admin/discount_events/discount_remove/<int:discount_id>',admin_views.discount_remove,name='discount_remove'),
    path('admin/customers',admin_views.customers,name='admin_customers'),
    path('admin/sellers',admin_views.sellers,name='admin_sellers'),
    path('admin/categories',admin_views.categories,name='admin_categories'),
    path('admin/categories/cat_remove/<int:cat_id>',admin_views.category_remove,name='category_remove'),
    path('admin/sellers/delete_seller/<int:delete_id>',admin_views.delete_seller,name='delete_seller'),
    path('admin/customers/add_seller',admin_views.add_seller,name='add_seller'),
    path('admin/products',admin_views.products,name='admin_products'),
    path('admin/products/remove_products/<int:product_id>',admin_views.remove_product,name='product_remove'),
    path('admin/orders',admin_views.orders,name='admin_orders'),
    path('admin/customers/add_customers',admin_views.add_customer,name='add_customer'),
    path('admin/remove_customers/<int:delete_id>',admin_views.delete_customer,name='delete_customer'),
    path('admin/customers/customer_details/<int:customer_id>',admin_views.customer_details, name='customer_details'),
    path('admin/sellers/seller_details/<int:vendor_id>',admin_views.seller_details,name='vendor_details'),
    path('admin/orders/order_details/<int:order_id>',admin_views.order_details,name='order_content'),




    path('',user_views.home,name='home'),
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
    path('seller_home/returns/',seller_views.returns,name='returns'),
    path('seller_registration/',seller_views.seller_registration,name='seller_registration'),
    path('seller_login/',seller_views.seller_login,name='seller_login'),
    path('seller_logout/',seller_views.seller_logout,name='seller_logout'),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paypal-reverse/',user_views.paypal_reverse,name='paypal_reverse'),
    path('paypal_cancel/',user_views.paypal_cancel,name='paypal_cancel'),






] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
