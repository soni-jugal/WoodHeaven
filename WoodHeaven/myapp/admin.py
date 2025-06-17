from django.contrib import admin
from .models import *
# Register your models here.


class showregister(admin.ModelAdmin):
    list_display = ['first_name','last_name','password','cpassword','email','phone']
admin.site.register(Register_table,showregister)


class showbrand(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(brand_table,showbrand)

class showproduct(admin.ModelAdmin):
    list_display = ['name','price','use_for','description','color','material','size','item_weight','dimensions','brand','admin_photo','available']
admin.site.register(Product_table,showproduct)



class showcomment(admin.ModelAdmin):
    list_display = ['product','name','email','phone','message','date']
admin.site.register(Comment_table,showcomment)


class showImage(admin.ModelAdmin):
    list_display = ['product','admin_photo1']
admin.site.register(ProductImage,showImage)

class showcarts(admin.ModelAdmin):
    list_display = ['user','product','quantity']
admin.site.register(Cart_Item,showcarts)


class showcheckout(admin.ModelAdmin):
    list_display = ['user','product','f_name','l_name','phone','email','address1','address2','city','district','zipcode','ordernote']
admin.site.register(checkout_table,showcheckout)


class showrating(admin.ModelAdmin):
    list_display = ['user','product','name','rating','review']
admin.site.register(Rating_table,showrating)

class showc(admin.ModelAdmin):
    list_display = ['code','discount','active']
admin.site.register(Coupon,showc)