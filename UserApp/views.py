from django.shortcuts import render,redirect
from django.db.models import Q
from SellerApp.models import *
from AdminApp.models import *
from UserApp.models import UserDataModel,CartDataModel,WishlistModel,UserAddressDataModel,ReviewDataModel,OrderDetailsModel
from .utils import product_rating,send_otp
from django.core.mail import send_mail
import pyotp
from paypal.standard.forms import PayPalPaymentsForm
import random

# Create your views here.

def home(request):
    def get_four_data(category):
        count = ProductModel.objects.filter(category_id__category_name=category).count()
        if count < 4:
            return ProductModel.objects.filter(category_id__category_name=category)
        random_index = random.randint(0, count - 4)
        return ProductModel.objects.filter(category_id__category_name=category)[random_index: random_index + 4]

    tv_data = get_four_data('television')
    laptop_data = get_four_data('laptop')
    phone_data = get_four_data('smartphone')
    category_data = ProductCategoryModel.objects.all()


    reordered_category_data = [
        category_data[2],
        category_data[4],
        category_data[1],
        category_data[3],
        category_data[0],
    ]

    event_data = EventModel.objects.all().order_by('-event_id')[:3]
    star_range = range(5)
    user_rating_half = None

    product_rating(tv_data)
    product_rating(laptop_data)
    product_rating(phone_data)

    user=None
    cart_no = None
    if 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id =request.session['user_id']).count()

    return render(request,'home.html',{'tv_data':tv_data,
                                                            'laptop_data':laptop_data,
                                                            'phone_data':phone_data,
                                                            'category_data':reordered_category_data,
                                                            'event_data':event_data,
                                                            'star_range':star_range,
                                                            'user_rating_half':user_rating_half,
                                                             'user': user,
                                                            'cart_no':cart_no})

def search_results(request):
    user = None
    cart_no =None
    if 'user_id' in request.session:
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
        user = UserDataModel.objects.get(user_id=request.session['user_id'])

    category_data = ProductCategoryModel.objects.all()
    product_data = ProductModel.objects.all()

    reordered_category_data = [
        category_data[2],
        category_data[4],
        category_data[1],
        category_data[3],
        category_data[0],
    ]
    search_term_mappings = {
        'mobile': 'Smartphone',
        'mobiles': 'Smartphone',
        'Mobile': 'Smartphone',
        'Mobiles': 'Smartphone',
        'audio' : 'Audio',
        'computer': 'Computer',
        'pc': 'Computer',
        'tv':'Television',
        'TV': 'Television',
        'Tv': 'Television',
        'television': 'Television',
        'laptop': 'Laptop',
    }


    if request.method == 'POST':
        search_data = request.POST.get('search-data', '')
        category_name = search_term_mappings.get(search_data)

        if 'priceRange' in request.POST:
            if category_name:
                price_ranges = request.POST.getlist('priceRange')
                price_ranges = [int(price) for price in price_ranges]
                product_data = product_data.filter(category__category_name__icontains=category_name,product_price__lt=min(price_ranges))
                brand_data = ProductBrandModel.objects.filter(category__category_name__icontains=category_name).distinct()
            else:
                price_ranges = request.POST.getlist('priceRange')
                price_ranges = [int(price) for price in price_ranges]
                product_data = product_data.filter(Q(product_name__icontains=search_data) | Q(product_brand__icontains=search_data) | Q(category__category_name__icontains=search_data),product_price__lt=min(price_ranges))
                brand_data = None

        elif category_name:
            product_data = product_data.filter(category__category_name__icontains=category_name)
            print(product_data)
            brand_data = ProductBrandModel.objects.filter(category__category_name__icontains=category_name).distinct()
        else:
            product_data = product_data.filter(Q(product_name__icontains=search_data) | Q(product_brand__icontains=search_data) | Q(category__category_name__icontains=search_data))
            print(product_data)
            brand_data = None

        star_range = range(5)
        user_rating_half = None
        product_rating(product_data)

    return render(request,'search-details.html',{'user': user,'category_data':reordered_category_data,'product_data':product_data,'star_range':star_range,'user_rating_half':user_rating_half,'search_data':search_data,'brand_data':brand_data,'cart_no':cart_no})

def contact(request):
    user = None
    cart_no = None
    if 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
        if request.method == "POST":
            name=request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            send_mail(
                "Regarding your recent inquiry",
                f"Hi {name},"
                f"We have received your message ({message[:10]}...). Our representative will be contacting you soon.",
                "techbuy97@gmail.com",
                [email],
                fail_silently=False

            )
            return redirect('contact')

    return render(request,'contactus.html',{'user':user,'cart_no':cart_no})

def about_us(request):
    user = None
    cart_no = None
    if 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
    return render(request,'aboutus.html',{'user':user,'cart_no':cart_no})

def category_function(request,cat_id):
    category_data = ProductCategoryModel.objects.all()
    reordered_category_data = [
        category_data[2],
        category_data[4],
        category_data[1],
        category_data[3],
        category_data[0],
    ]
    current_category_data = ProductCategoryModel.objects.filter(category_id=cat_id)
    brand_data = ProductBrandModel.objects.filter(category_id=cat_id)
    product_data = ProductModel.objects.filter(category_id=cat_id)
    star_range = range(5)
    user_rating_half = None
    product_rating(product_data)
    event_data = EventModel.objects.filter(event_category_id=cat_id)
    if cat_id == 3:
        event_data = event_data.order_by('-event_id')[:2]
    else:
        event_data = event_data.order_by('-event_id')[:3]

    user = None
    cart_no = None
    if 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id = request.session['user_id']).count()

    return render(request,'category_template.html',{'category_data': reordered_category_data,
                                                                        'brand_data':brand_data,
                                                                        'product_data':product_data,
                                                                        'cat_id': cat_id,
                                                                        'category_name':current_category_data,
                                                                        'event_data':event_data,
                                                                        'star_range':star_range,
                                                                        'user_rating_half':user_rating_half,
                                                                        'user':user,
                                                                        'cart_no':cart_no})

def product_details(request,pro_id):
    product_data = ProductModel.objects.filter(product_id=pro_id)
    product_obj = ProductModel.objects.get(product_id=pro_id)

    reviews_data = ReviewDataModel.objects.filter(product=product_obj)
    review_count = reviews_data.count()
    filled_review_counts = reviews_data.exclude(user_review__isnull=True).exclude(user_review__exact='').count()

    total_user_rating = 0
    for rating in reviews_data:
        total_user_rating += rating.user_rating
    if review_count >0:
        avg_user_rating = total_user_rating / review_count
        product_obj.user_rating = avg_user_rating
        product_obj.save()


    cat_id = product_obj.category_id
    category_data = ProductCategoryModel.objects.all()
    reordered_category_data = [
        category_data[2],
        category_data[4],
        category_data[1],
        category_data[3],
        category_data[0],
    ]
    star_range = range(5)
    user_rating_half = None

    product_rating(product_data)

    spec_storage=0
    for i in product_data:
        if cat_id==5:
            for spec in i.computer.all():
                if spec.spec_storage/1000 >= 1000:
                    spec_storage=spec.spec_storage/1000000
                else:
                    spec_storage=spec.spec_storage/1000
        elif cat_id==2:
            for spec in i.computer.all():
                if spec.spec_storage/1000 >= 1000:
                    spec_storage=spec.spec_storage/1000000
                else:
                    spec_storage=spec.spec_storage/1000

    cat_name = product_obj.category.category_name
    count=ProductModel.objects.filter(category_id__category_name=cat_name).count()
    product_set={}
    if count >= 4:
        random_index = random.randint(0,count-4)
        product_set=ProductModel.objects.filter(category_id__category_name=cat_name)[random_index:random_index+4]
    else:
        product_set = ProductModel.objects.filter(category_id__category_name=cat_name)

    user = None
    cart_no = None
    if 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()


    if request.method == "POST":
        if 'user_id' in request.session:
            user = UserDataModel.objects.get(user_id=request.session['user_id'])
            if "addtocart" in request.POST:
                cart_obj = CartDataModel()
                cart_obj.user = user
                cart_obj.product = product_obj
                cart_obj.save()
                return redirect('cart')
            elif "wishlist" in request.POST:
                wish_obj = WishlistModel()
                wish_obj.user = user
                wish_obj.product =product_obj
                wish_obj.save()
                return redirect('my_wishlist')
            elif 'rating' in request.POST or 'review' in request.POST:
                rating = request.POST.get('rating')
                review = request.POST.get('review')
                review_obj = ReviewDataModel()
                review_obj.product = product_obj
                review_obj.user = user
                review_obj.user_review = review
                review_obj.user_rating = rating
                review_obj.save()
                return redirect('product_details', pro_id=pro_id)
        else:
            return redirect('login')

    return render(request,'product-details.html',{'product_data':product_data,
                                                                       'category_data':reordered_category_data,
                                                                       'star_range':star_range,
                                                                        'user_rating_half':user_rating_half,
                                                                        'cat_id': cat_id,
                                                                        'product_obj':product_obj,
                                                                        'spec_storage':spec_storage,
                                                                        'product_set':product_set,
                                                                        'user':user,
                                                                        'reviews_data':reviews_data,
                                                                        'review_count': review_count,
                                                                        'filled_review_counts':filled_review_counts,
                                                                        'cart_no':cart_no})

def sign_up(request):
    user_error = ''
    pass_error = ''
    email_error = ''
    phno_error = ''
    first_name = ''
    last_name = ''
    username = ''
    email = ''
    user_phone = ''
    if request.method=="POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('user_email')
        password = request.POST.get('user_pass')
        cpassword = request.POST.get('user_cpass')
        user_phone = request.POST.get('user_phn')

        if UserDataModel.objects.filter(user_name=username).exists():
            user_error='Username already exists. Please choose another username.'

        if UserDataModel.objects.filter(user_email=email).exists():
            email_error='Email already exists. Please Login'

        if UserDataModel.objects.filter(user_phone=user_phone).exists():
            phno_error='Phone number already exists.'

        if password != cpassword:
            pass_error = "Password doesn't match. Please re-enter"

        if user_error or email_error or phno_error or pass_error:
            return render(request, 'signup.html', {
                'user_error': user_error,
                'email_error': email_error,
                'phno_error': phno_error,
                'pass_error': pass_error,
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'user_phone': user_phone
            })
        user_obj = UserDataModel()
        user_obj.user_first_name = first_name
        user_obj.user_last_name = last_name
        user_obj.user_name = username
        user_obj.user_email = email
        user_obj.user_phone = user_phone
        user_obj.user_password = cpassword
        user_obj.save()

        return redirect('login')

    return render(request, 'signup.html',{'user_error': user_error,'email_error': email_error,'phno_error': phno_error,'pass_error': pass_error,'first_name':first_name,'last_name':last_name,'username':username,'email':email,'user_phone':user_phone})

def login(request):
    error=''
    if request.method=="POST":
        username = request.POST.get('user_name')
        user_password = request.POST.get('user_pass')
        user_data = UserDataModel.objects.filter(user_name=username,user_password=user_password).first()
        if user_data is not None:
            request.session['user_id']=user_data.user_id
            return redirect('home')
        else:
            error="Invalid Username or Password"

    return render(request,'login.html', {'error':error})

def dashboard(request):
    user = None
    cart_no = None
    if 'user_id' not in request.session:
        return redirect('home')
    elif 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
        if request.method == "POST" and 'profile_upd' in request.FILES:
            profile_pic = request.FILES.get("profile_upd")
            user.user_profile_img = profile_pic
            user.save()
    return render(request, 'dashboard.html', {'user': user,'cart_no':cart_no})


def cart(request):
    user = None
    product = None
    if 'user_id' not in request.session:
        return redirect('home')
    elif 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_data = CartDataModel.objects.filter(user=user)
        cart_count = cart_data.count()
        total_price= 0
        total_discount = 0
        for item in cart_data:
            total_price += item.cart_quantity * item.product.product_price
        for i in cart_data:
            if i.product.has_discount:
                discount_amount_per_product = i.product.product_price - i.product.discount_price()
                total_discount += i.cart_quantity * discount_amount_per_product
        net_amount = total_price-total_discount

        if request.method == "POST":
            cart_id = request.POST.get('cart_id')
            product_data = request.POST.get('product_data')
            product = ProductModel.objects.get(product_id=product_data)
            cart_obj = CartDataModel.objects.get(cart_id=cart_id)

            if 'cart_add' in request.POST:
                cart_obj.cart_quantity += 1
            elif 'cart_min' in request.POST and cart_obj.cart_quantity > 0:
                cart_obj.cart_quantity -= 1

            cart_obj.user = user
            cart_obj.product = product
            cart_obj.save()
            return redirect('cart')

    return render(request,'cart.html',{'user':user,'cart_data':cart_data,'cart_count':cart_count,'total_price':total_price,'total_discount':total_discount,'net_amount':net_amount,'product_obj':product})

def cart_remove(request,cart_id):
    cart_obj = CartDataModel.objects.get(cart_id=cart_id)
    cart_obj.delete()
    return redirect('cart')

def cart_save(request,cart_id):
    user = UserDataModel.objects.get(user_id=request.session['user_id'])
    cart_obj = CartDataModel.objects.get(cart_id=cart_id)
    cart_obj.delete()
    wish_obj = WishlistModel()
    wish_obj.user = user
    wish_obj.product = cart_obj.product
    wish_obj.save()
    return redirect('my_wishlist')



def my_account(request):
    user = None
    cart_no = None
    if 'user_id' not in request.session:
        return redirect('home')
    elif 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
        if request.method == "POST":
            if 'profile_upd' in request.FILES:
                profile_pic = request.FILES.get("profile_upd")
                user.user_profile_img = profile_pic
                user.save()
            elif 'username_btn' in request.POST:
                username = request.POST.get('username')
                user.user_name = username
                user.save()

    return render(request,'my_account.html',{'user':user,'cart_no':cart_no})


def change_password(request):
    password_error = None
    otp_error = None
    password_success = None

    if 'user_id' in request.session:
        user_id = int(request.session['user_id'])
        user_obj = UserDataModel.objects.get(user_id=user_id)

        if request.method == "POST":
            if 'verify' in request.POST:
                new_password = request.POST.get('password')
                confirm_password = request.POST.get('confirmPassword')

                if new_password != confirm_password:
                    password_error = "Passwords don't match"
                else:
                    request.session['new_password'] = new_password
                    otp_gen = send_otp(request)
                    send_mail(
                        "OTP to change password",
                        f"OTP to change password: {otp_gen}",
                        'techbuy97@gmail.com',
                        [user_obj.user_email],
                        fail_silently=False
                    )
                    password_success = True

            elif 'submit' in request.POST:
                otp_submit = request.POST.get('otp')
                otp_key = request.session.get('otp_key', '')

                if otp_key:
                    totp = pyotp.TOTP(otp_key, interval=300)
                    if totp.verify(otp_submit):
                        new_password = request.session['new_password']
                        user_obj.user_password = new_password
                        user_obj.save()
                        del request.session['otp_key']
                        del request.session['new_password']
                        return redirect('my_account')
                    else:
                        otp_error = "Invalid OTP"
                else:
                    otp_error = "OTP not generated properly"

    else:
        return redirect('login')

    return render(request, 'change-password.html', {'password_error': password_error,'otp_error': otp_error,'password_success': password_success})
def my_address(request):
    user = None
    cart_no = None
    if 'user_id' not in request.session:
        return redirect('home')
    elif 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()

    address_data = UserAddressDataModel.objects.filter(user=user)

    if request.method == "POST":
        if 'new_address' in request.POST:
            address_name = request.POST.get('address_name')
            address = request.POST.get('useraddress')
            pincode = request.POST.get('userpin')
            district = request.POST.get('userdistrict')
            state = request.POST.get('userstate')
            phno = request.POST.get('userphno')
            address_obj = UserAddressDataModel()
            address_obj.user = user
            address_obj.address_name = address_name
            address_obj.house_address = address
            address_obj.pincode_address = pincode
            address_obj.city_address = district
            address_obj.state_address = state
            address_obj.phone_no = phno
            address_obj.save()

            return redirect('my_address')

        elif 'editaddress' in request.POST:
            address_id = int(request.POST.get('address_id'))
            address_name = request.POST.get('address_name')
            address = request.POST.get('useraddress')
            pincode = request.POST.get('userpin')
            district = request.POST.get('userdistrict')
            state = request.POST.get('userstate')
            phno = request.POST.get('userphno')
            address_obj = UserAddressDataModel.objects.get(address_id = address_id)
            address_obj.user = user
            address_obj.address_name = address_name
            address_obj.house_address = address
            address_obj.pincode_address = pincode
            address_obj.city_address = district
            address_obj.state_address = state
            address_obj.phone_no = phno
            address_obj.save()

            return redirect('my_address')


    return render(request,'myaddress.html',{'user':user,'address_data':address_data,'cart_no':cart_no})

def delete_address(request,add_id):
    add_obj = UserAddressDataModel.objects.get(address_id=add_id)
    add_obj.delete()
    return redirect('my_address')

def my_orders(request):
    user = None
    cart_no = None
    if 'user_id' not in request.session:
        return redirect('home')
    elif 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        order_data = OrderDetailsModel.objects.filter(user=user)
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
        if request.method == "POST":
            if 'cash_on_delivery' in request.POST:
                product_data = ProductModel.objects.get(product_id=int(request.POST.get('product')))
                user_data = user
                address_data = UserAddressDataModel.objects.get(address_id=int(request.session['address_id']))
                order_quantity = int(request.session['quantity'])
                cost_data = int(request.POST.get('cost'))
                order_obj = OrderDetailsModel()
                order_obj.product = product_data
                order_obj.user = user_data
                order_obj.address = address_data
                order_obj.user_order_quantity = order_quantity
                order_obj.order_cost = cost_data
                order_obj.payment_method = request.POST.get('payment')
                order_obj.save()
                cart_id = request.session.get('cart_id', None)
                if cart_id is not None:
                    cart_obj = CartDataModel.objects.get(cart_id = int(cart_id))
                    cart_obj.delete()
                    del request.session['cart_id']

                return redirect('my_orders')
            if 'cancel_order' in request.POST:
                order_obj = OrderDetailsModel.objects.get(user_order_id=request.POST.get('order_id'))
                order_obj.status = "cancelled"
                order_obj.save()
                return redirect('my_orders')

    return render(request,'myorders.html',{'user':user,'cart_no':cart_no,'order_data':order_data})

def my_payments(request):
    user = None
    cart_no = None
    if 'user_id' not in request.session:
        return redirect('home')
    elif 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
    return render(request,'payments.html',{'user':user,'cart_no':cart_no})

def my_wishlist(request):
    user = None
    cart_no = None
    if 'user_id' not in request.session:
        return redirect('home')
    elif 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()

    wish_data = WishlistModel.objects.filter(user=user)

    if request.method=="POST":
        if "add_cart" in request.POST:
            user_data = user
            product_data = request.POST.get('product_data')
            cart_obj = CartDataModel()
            cart_obj.user = user_data
            cart_obj.product = ProductModel.objects.get(product_id=product_data)
            cart_obj.save()
            wish_id = request.POST.get('wishlist_data')
            wish_obj= WishlistModel.objects.get(wishlist_id=wish_id)
            wish_obj.delete()

            return redirect('cart')

    return render(request,'wishlist.html',{'user':user,'wish_data':wish_data,'cart_no':cart_no})

def remove_wishlist(request,wish_id):
    wish_obj =WishlistModel.objects.get(wishlist_id=wish_id)
    wish_obj.delete()
    return redirect('my_wishlist')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')

def deactivate(request,user_id):
    user_obj = UserDataModel.objects.get(user_id=user_id)
    del request.session['user_id']
    user_obj.delete()
    return redirect('home')

def store_locations(request):
    user = None
    cart_no = None
    if 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
    return render(request,'store_locator.html',{'user':user,'cart_no':cart_no})

def purchase_product(request,product_id):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user = UserDataModel.objects.get(user_id= user_id)
        product_obj = ProductModel.objects.get(product_id=product_id)
        address_data = UserAddressDataModel.objects.filter(user=user)
        address_data_check = UserAddressDataModel.objects.filter(user=user).exists()
        quantity = 1
        total_price = product_obj.product_price * quantity
        total_discount_price = product_obj.discount_price() * quantity
        total_discount = total_price - total_discount_price
        current_address = None
        if address_data is not None:
            first_address = address_data.first()
            request.session['address_id'] = first_address.address_id
            address_id = int(request.session['address_id'])
            current_address = UserAddressDataModel.objects.get(address_id=address_id)
        if request.method == "POST":
            if 'del_add_change' in request.POST:
                selected_address_id = request.POST.get('address_input')
                request.session['address_id'] = selected_address_id
                address_id = int(request.session['address_id'])
                current_address = UserAddressDataModel.objects.get(address_id=address_id)
            if 'quantity' in request.POST:
                quantity = int(request.POST.get('quantity'))
                request.session['quantity'] = quantity
            else:
                quantity = request.session.get('quantity', 1)
            if 'cart_id' in request.POST:
                cart_id = int(request.POST.get('cart_id'))
                request.session['cart_id'] = cart_id

            total_price = product_obj.product_price * quantity
            total_discount_price = product_obj.discount_price() * quantity
            total_discount = total_price - total_discount_price

            return render(request, 'buy_now.html',{'user': user, 'product_obj': product_obj, 'discounted_price': total_discount_price,'quantity': quantity, 'total_price': total_price, 'total_discount': total_discount,'address_data':address_data, 'address_data_check':address_data_check , 'current_address': current_address})

        return render(request, 'buy_now.html', {'user': user, 'product_obj': product_obj, 'discounted_price': total_discount_price,'quantity':quantity,'total_price':total_price,'total_discount':total_discount,'address_data':address_data, 'address_data_check':address_data_check ,'current_address':current_address})
