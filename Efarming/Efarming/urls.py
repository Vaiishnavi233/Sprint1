from django.contrib import admin
from django.urls import path

from farmerapp import views
from farmerapp.payment import original_payment, payment_status
from farmerapp.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name="home"),
    path('signup',Signup,name="signup"),
	path('about/',About,name='about'),
	path('contact/',Contact,name='contact'),
    path('login/',Login,name="login"),
    path('logoutuser',Logout,name="logout"),
    path('view_user',View_user,name="view_user"),
    path('add_product',Add_Product,name="add_product"),
    path('view_feedback', View_feedback, name='view_feedback'),
    path('view_product/<int:pid>/', View_prodcut, name='view_product'),

    path('admin_view_product', Admin_View_product, name='admin_view_product'),
    path('login_admin',Admin_Login,name="login_admin"),
    path('admin_viewBooking', Admin_View_Booking, name='admin_viewBooking'),
    path('view_categary/', View_Categary, name='view_categary'),
    path('add_categary', Add_Categary, name='add_categary'),
    path('add_cart(?P<int:pid>)', Add_Cart, name='add_cart'),
    path('delete_product(?P<int:pid>)', delete_product, name='delete_product'),
    path('delete_user(?P<int:pid>)', delete_user, name='delete_user'),
    path('delete_feedback(?P<int:pid>)', delete_feedback, name='delete_feedback'),
    path('cart', view_cart, name='cart'),
    path('payment(?P<book>[0-9]+)', payment, name='payment'),
    path('delete_booking/(?P<str:pid>)/(?P<bid>[0-9]+)', delete_booking, name='delete_booking'),
    path('delete_admin_booking/(?P<str:pid>)/(?P<bid>[0-9]+)', delete_admin_booking, name='delete_admin_booking'),
    path('booking_detail/<uuid:pid>/<int:bid>/', views.booking_detail, name='booking_detail'),
    #path('booking_detail/(?P<str:pid>)/(?P<bid>[0-9]+)', booking_detail, name='booking_detail'),
    path('admin_booking_detail/(?P<str:pid>)/(?P<bid>[0-9]+)/(?P<uid>[0-9]+)', admin_booking_detail, name='admin_booking_detail'),
    path('Edit_status/(?P<str:pid>)/(?P<bid>[0-9]+)', Edit_status, name='Edit_status'),
    path('remove_cart(?P<int:pid>)', remove_cart, name='remove_cart'),
    path('booking/<str:pid>/', Booking_order, name="booking"),
    path('view_booking', View_Booking, name='view_booking'),
    path('profile/<int:pid>/', profile, name='profile'),
    path('edit_profile/', Edit_profile, name='edit_profile'),
    path('delete_category(?P<int:pid>)', delete_category, name='delete_category'),
    path('admin_home', Admin_Home, name='admin_home'),
    path('change_password', Change_Password, name="change_password"),
    path('payment_status/', payment_status, name="payment_status"),
    path('original_payment/', original_payment, name="original_payment"),
    path('view_farmer/', View_farmer, name="view_farmer"),
    path('change_user_status/<int:pid>', change_user_status, name="change_user_status"),
    path('send_feedback/(?P<pid>[0-9]+)', Feedback, name='send_feedback'),
    path('product_detail/<int:pid>', product_detail, name='product_detail'),
    path('farmer_detail/<int:pid>', farmer_detail, name='farmer_detail'),
    path('payment/', views.payment_page, name='payment_page'),
    path('cod/<int:cart_id>/', views.cash_on_delivery, name='cash_on_delivery'),
   ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
