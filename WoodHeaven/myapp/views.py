import json
import string

from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login,update_session_auth_hash

import json
from django.http import HttpResponse,JsonResponse


def indexpage(request):
    user = request.session.get('logid')
    if user:
        getdata=Cart_Item.objects.filter(user=user)
        qty=sum(item.quantity for item in getdata)
        return render(request,"index.html",{'qty':qty})

    # getall = Product_table.objects.all()
    # getbrand = brand_table.objects.get(name="Nilkamal")
    # getdata = Product_table.objects.filter(brand=getbrand)
    # context={'getall':getall,'getdata':getdata}
    return render(request,"index.html")

def blogpage(request):
    return render(request,"blog.html")

def categorypage(request):
    brand = brand_table.objects.all()
    brandid = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    # Filter by brand if brandid is provided
    if brandid:
        product = Product_table.objects.filter(brand=brandid)
    else:
        product = Product_table.objects.all()






    if sort_by == 'price':
        product = product.order_by('price')
    elif sort_by == 'name':
        product = product.order_by('name')
    elif sort_by == 'color':
        product=product.order_by('color')
    else:
        product = product.order_by('id')






    if not product.exists():
        not_found = True
        messages.warning(request, "PRODUCT NOT FOUND")
    else:
        not_found = False



    getlen = len(product)

    return render(request, "category.html", {
        'getdata': product,
        'brand': brand,
        'not_found': not_found,
        'getlen': getlen
    })





def confirmationpage(request):
    user=request.session['logid']
    getdata=checkout_table.objects.filter(user=user)

    return render(request,"confirmation.html",{'getdata':getdata})

def elementspage(request):
    return render(request,"elements.html")

def featurepage(request):
    return render(request,"feature.html")

def loginpage(request):
    return render(request,"login.html")


def fetchloginpage(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            checkuser=Register_table.objects.get(email=email,password=password)
            request.session["logid"]=checkuser.id
            request.session['logname']=checkuser.first_name
        except: checkuser=None
        if checkuser is not None:
            return redirect("/")
        else:
            messages.warning(request,"email or password is not match please try again........")
            return render(request,"login.html")

    return redirect("/")





def logout(request):
    try:
        del request.session['logid']
        del request.session['logname']
    except:
        pass
    return redirect("/")

def single_blogpage(request):
    return render(request,"single-blog.html")


import random


def singleproductpage(request, id):
    singleproduct = Product_table.objects.get(id=id)
    product_images = ProductImage.objects.filter(product=singleproduct)

    getratingdata=Rating_table.objects.filter(product=id)

    comments = Comment_table.objects.filter(product=singleproduct)
    for comment in comments:
        comment.randomcolor = random.choice(['orange', 'blue', 'black', 'green', 'marron','red','pink','grey'])


    if singleproduct.available=='in-stock':
        found_stock=True
    else:
        found_stock=False





    return render(request, "single-product.html", {
        'singledata': singleproduct,
        'product_images': product_images,
        'comments': comments,
        'found_stock':found_stock,
        'getrat':getratingdata
    })

def trackingpage(request):
    return render(request,"tracking.html")

def registerpage(request):
    return render(request,"register.html")

def fetchregisterpage(request):
    first_name=request.POST.get('fname')
    last_name=request.POST.get('lname')
    password=request.POST.get('password')
    cpassword=request.POST.get('cpassword')
    email=request.POST.get('email')
    phone=request.POST.get('phone')
    if Register_table.objects.filter(email=email).exists():
        messages.error(request,"user is already taken")
        return render(request,"register.html")
    if password != cpassword:
        messages.error(request,"Password is not match...")
        return render(request,"register.html")
    if phone:
        if int(len(phone))>10:
            messages.error(request, "Enter Valid 10-digit Mobile Number...")
            return render(request, "register.html")

    storedata=Register_table(first_name=first_name,last_name=last_name,password=password,cpassword=cpassword,email=email,phone=phone)
    storedata.save()
    return redirect("/login.html")



def cartpage(request):
    return render(request,"cart.html")



def contactpage(request):
    return render(request,"contact.html")



def commentpage(request):
    product=request.POST.get('product')
    name=request.POST.get('name')
    email=request.POST.get('email')
    phone=request.POST.get('phone')
    message=request.POST.get('message')
    storedata=Comment_table(product=Product_table(id=product),name=name,email=email,phone=phone,message=message)
    storedata.save()
    return redirect('/category.html')



def add_to_cart(request,id):
    if "logid" not in request.session:
        messages.info(request, "Please log-in first to add items to the cart.")
        return redirect('/login.html')
    product=Product_table.objects.get(id=id)

    user=request.session['logid']
    cart,created=Cart_Item.objects.get_or_create(product=product,user=Register_table(id=user))
    if not created:
        cart.quantity+=1
    cart.save()

    return redirect("/category.html")



def showcart(request):
    if "logid" not in request.session:
        messages.error(request,"Please Login to Access your Cart!!!")
        context={'logged_in':False}
        return render(request,"cart.html",context)
    user=request.session['logid']
    cart_item=Cart_Item.objects.filter(user=Register_table(id=user))
    total=0
    for i in cart_item:
        i.total_price=i.product.price*i.quantity
        total+=i.total_price

    sgst=sum(round(item.total_price/21) for item in cart_item)
    gst=sum(round(item.total_price/30) for item in cart_item)
    if cart_item:
        delivery_charges=100
    else:
        delivery_charges=0
    grand_total=total+sgst+gst+delivery_charges
    if not cart_item:
        not_found = True
    else:
        not_found = False
    context={
        'cart_item':cart_item,
        'total':total,
        'sgst':sgst,
        'gst':gst,
        'delivery_charges':delivery_charges,
        'grand_total':grand_total,
        'not_found':not_found,
        'logged_in':True
    }

    return render(request,"cart.html",context)

def update_cart(request,id,action):
    user = request.session['logid']
    cart_item=Cart_Item.objects.get(id=id,user=Register_table(id=user))
    if action=='increment':
        cart_item.quantity+=1
    elif action=='decrement':
        if cart_item.quantity>1:
            cart_item.quantity-=1
    cart_item.save()
    return redirect("showcart")





def removecartitem(request,id):
    removedata=Cart_Item.objects.get(id=id)
    removedata.delete()
    return redirect("/")



def removeallcartitem(request):
    removedata=Cart_Item.objects.all()
    removedata.delete()
    return redirect("/")

def findchair(request):
    cname=request.POST.get('cname')
    cname1=string.capwords(cname)
    product=Product_table.objects.filter(name__icontains=cname1)
    if not product:
        not_founds = True
        messages.warning(request, "PRODUCT NOT FOUND")

    else:
        not_founds = False
    getlen = len(product)
    # if len(product)>1:
    #     getlen=product
    return render(request,"category.html",{'getdata':product,'not_founds':not_founds,'getlen':getlen})




def checkoutpage(request):
    if "logid" not in request.session:
        messages.warning(request,"Please Login First For Checkout")
        context={'founded_in':False}
        return render(request,"checkout.html",context)
    userid=request.session['logid']
    cart_item=Cart_Item.objects.filter(user=userid)
    total = 0
    for i in cart_item:
        i.total_price = i.product.price * i.quantity
        total += i.total_price

    sgst = sum(round(item.total_price / 21) for item in cart_item)
    gst = sum(round(item.total_price / 30) for item in cart_item)

    if cart_item:
        delivery_charges = 100
    else:
        delivery_charges = 0
    grand_total = total + sgst + gst + delivery_charges


    context = {
        'getdata': cart_item,
        'total': total,
        'sgst': sgst,
        'gst': gst,
        'delivery_charges': delivery_charges,
        'grand_total': grand_total,
        'founded_in':True,

    }


    return render(request,"checkout.html",context)





def fetchcheckoutdata(request):
    user=request.session['logid']
    product=request.POST.get('product')
    fname=request.POST.get('fname')
    lname=request.POST.get('lname')
    phone=request.POST.get('phone')
    email=request.POST.get('email')
    address1=request.POST.get('add1')
    address2=request.POST.get('add2')
    city=request.POST.get('city')
    district=request.POST.get('district')
    zipcode=request.POST.get('zipcode')
    ordernote=request.POST.get('message')


    storedata=checkout_table(user=Register_table(id=user),product=Cart_Item(id=product),f_name=fname,l_name=lname,phone=phone,email=email,address1=address1,address2=address2,city=city,district=district,zipcode=zipcode,ordernote=ordernote)
    storedata.save()
    messages.success(request,"Your Order is Confirm")
    return redirect("confirmation.html")


def reviewpage(request,id):
    if "logid" not in request.session:
        messages.info(request, "Please log-in first to adding reviews.")
        return redirect('/login.html')
    return render(request,"review.html",{'id':id})


def fetchreviewpage(request):
    user=request.session['logid']
    product=request.POST.get('product')
    name=request.POST.get('name')
    rating=request.POST.get('rating')
    review=request.POST.get('review')
    storedata=Rating_table(user=Register_table(id=user),product=Product_table(id=product),name=name,rating=rating,review=review)
    storedata.save()
    return redirect("category.html")



def apply_coupon(request):
    if request.method == "POST":
        data=json.loads(request.body)
        coupon_code=data.get('coupon_code')
        try:
            coupon=Coupon.objects.get(code=coupon_code)
            if coupon.active:
                response={'valid':True,'discount':float(coupon.discount)}
            else:
                response={'valid':False,'error':'Already used'}
        except Coupon.DoesNotExist:
            response={'valid':False,'error':'Coupon Dose Not Exist'}
        return JsonResponse(response)
    return JsonResponse({'valid': False, 'error': 'Invalid request method.'})


