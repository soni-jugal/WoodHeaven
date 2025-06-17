from django.db import models

from django.utils.safestring import mark_safe


class Register_table(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    password=models.CharField(max_length=40)
    cpassword=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.BigIntegerField()
    def __str__(self):
        return self.first_name
class brand_table(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product_table(models.Model):
    AVAILABLE=[
        ('in-stock','in-stock'),
        ('out-of-stock','out-of-stock'),
    ]
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    use_for=models.CharField(max_length=40)
    description=models.TextField()
    color=models.CharField(max_length=100)
    material=models.CharField(max_length=100)
    size=models.CharField(max_length=100)
    item_weight=models.CharField(max_length=100)
    dimensions=models.CharField(max_length=100)
    brand=models.ForeignKey(brand_table,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='photos')
    available = models.CharField(max_length=100, choices=AVAILABLE)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    admin_photo.allow_tags = True

    def __str__(self):return self.name


class Comment_table(models.Model):
    product=models.ForeignKey(Product_table,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    phone=models.BigIntegerField(null=True)
    message=models.TextField(null=True)
    date=models.DateTimeField(auto_now_add=True,null=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product_table, on_delete=models.CASCADE, related_name='images',null=True)
    image = models.ImageField(upload_to='photos',null=True)

    def admin_photo1(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    admin_photo1.allow_tags = True

    def __str__(self):
        return self.product.name

class Cart_Item(models.Model):
    user=models.ForeignKey(Register_table,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product_table,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=1,null=True)
    def __str__(self):
        return self.product.name


class checkout_table(models.Model):
    user=models.ForeignKey(Register_table,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Cart_Item,on_delete=models.CASCADE,null=True)
    f_name=models.CharField(max_length=100,null=True)
    l_name=models.CharField(max_length=100,null=True)
    phone=models.BigIntegerField(null=True)
    email=models.EmailField(null=True)
    address1=models.TextField(null=True)
    address2=models.TextField(null=True)
    city=models.CharField(max_length=100,null=True)
    district=models.CharField(max_length=100,null=True)
    zipcode=models.IntegerField(null=True)
    ordernote=models.TextField(null=True)
    def __str__(self):
        return self.f_name


class Rating_table(models.Model):
    user=models.ForeignKey(Register_table,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product_table,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True)
    rating=models.IntegerField(null=True)
    review=models.TextField(null=True)




class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True, null=True)
    discount = models.IntegerField(null=True)
    active = models.BooleanField(default=True, null=True)

from django import forms
class CouponForm(forms.ModelForm):
    class Meta:
        modal=Coupon
        fields=['code']
