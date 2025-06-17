from django.urls import path
from . import views

urlpatterns=[
    path('',views.indexpage),
    path('blog.html',views.blogpage),
    path('category.html',views.categorypage),
    path('confirmation.html',views.confirmationpage),
    path('elements.html',views.elementspage),
    path('feature.html',views.featurepage),
    path('login.html',views.loginpage),
    path('single-blog.html',views.single_blogpage),
    path('single-product.html/<int:id>/',views.singleproductpage),
    path('cart.html',views.cartpage),
    path('checkout.html',views.checkoutpage),
    path('contact.html',views.contactpage),
    path('register.html',views.registerpage),
    path('fetchregisterpage',views.fetchregisterpage),
    path('fetchloginpage',views.fetchloginpage),
    path('logout',views.logout),
    path('commentpage',views.commentpage),
    path('add_to_cart/<int:id>/',views.add_to_cart,name="add_to_cart"),
    path('showcart',views.showcart,name="showcart"),
    path('update-cart/<int:id>/<str:action>/',views.update_cart,name='update_cart'),
    path('removecartitem/<int:id>/',views.removecartitem),
    path('findchair',views.findchair),
    path('removeallcartitem',views.removeallcartitem),
    path('fetchcheckoutdata',views.fetchcheckoutdata),
    path('reviewpage/<int:id>/',views.reviewpage),
    path('fetchreviewpage',views.fetchreviewpage),
    path('apply-coupon/', views.apply_coupon),



]