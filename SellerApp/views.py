from django.shortcuts import render,redirect
from django.core.mail import send_mail
from .utils import send_otp
from django.contrib import messages
import pyotp
from datetime import datetime, timedelta
from django.db.models import Q
from SellerApp.models import *
from UserApp.models import OrderDetailsModel
from AdminApp.models import ProductCategoryModel

# Create your views here.
def home(request):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller_obj = SellerDataModel.objects.get(seller_id=seller_id)
        product_data = ProductModel.objects.filter(seller=seller_obj)
        product_active = product_data.filter(product_status='active').count()
        product_inactive = product_data.filter(product_status='inactive').count()
        new_orders = OrderDetailsModel.objects.filter(product__seller__seller_id = seller_id ,status = 'dispatched').count()
        cancelled_orders = OrderDetailsModel.objects.filter(product__seller__seller_id = seller_id ,status = 'cancelled').count()
        low_stock=0
        no_stock=0
        for data in product_data:
            if data.seller_product_stock ==0:
                no_stock +=1
            elif data.seller_product_stock <=10:
                low_stock +=1
        return render (request,'seller_dashboard.html',{'seller':seller_obj,'product_active':product_active,'product_inactive':product_inactive,'low_stock':low_stock,'no_stock':no_stock,'new_orders':new_orders,'cancelled_orders':cancelled_orders})
    else:
        return redirect('seller_login')


def account_details(request):
    email_error = None
    phone_error = None
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller_obj = SellerDataModel.objects.get(seller_id=seller_id)
        if request.method=="POST":
            if 'user_personal' in request.POST:
                company_name = request.POST.get('user_name')
                user_address = request.POST.get('user_address')
                email = request.POST.get('user_email')
                phone = request.POST.get('user_phone')
                if SellerDataModel.objects.filter(seller_email=email).exclude(seller_id=seller_obj.seller_id).exists():
                    email_error = "You can't use that email because it's already in use"
                elif SellerDataModel.objects.filter(seller_phone=phone).exclude(seller_id=seller_obj.seller_id).exists():
                    phone_error = "You can't use that Phone number because it's already in use"
                if email_error or phone_error:
                    return render(request, 'seller_profile.html',{'seller': seller_obj, 'email_error': email_error, 'phone_error': phone_error})
                seller_obj.seller_company_name = company_name
                seller_obj.seller_address = user_address
                seller_obj.seller_email = email
                seller_obj.seller_phone = phone
                seller_obj.save()
                return redirect('seller_details')
            if 'user_bank' in request.POST:
                account_no = request.POST.get('user_account')
                bank_ifsc = request.POST.get('user_ifsc')
                seller_obj.seller_bank_acc = account_no
                seller_obj.seller_IFSC = bank_ifsc
                seller_obj.save()
                return redirect('seller_details')

        return render(request, 'seller_profile.html', {'seller': seller_obj})
    else:
        return redirect('seller_login')

def my_listing(request):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller_obj = SellerDataModel.objects.get(seller_id=seller_id)
        product_data = ProductModel.objects.filter(seller=seller_obj)
        product_active = product_data.filter(product_status='active').count()
        product_inactive = product_data.filter(product_status='inactive').count()
        category_data = ProductCategoryModel.objects.all()
        low_stock = 0
        no_stock = 0
        for data in product_data:
            if data.seller_product_stock == 0:
                no_stock += 1
            elif data.seller_product_stock <= 10:
                low_stock += 1

        search_data=''
        category_select=0
        status_select=''

        if request.method=='POST':
            if 'search_btn' in request.POST:
                search_data = request.POST.get('search-bar','')

                if search_data:
                    product_data = product_data.filter(Q(product_name__icontains=search_data) | Q(product_brand__icontains=search_data))


            elif 'category_filter' in request.POST or 'status_filter' in request.POST :
                category_select = request.POST.get('category_filter')
                status_select = request.POST.get('status_filter')
                search_data = request.POST.get('search-bar', '')
                if category_select != 'all':
                    if category_select and category_select.isdigit():
                        category_select = int(category_select)
                        product_data = product_data.filter(category__category_id=category_select)

                if status_select == 'active':
                    product_data = product_data.filter(product_status='active')
                elif status_select == 'inactive':
                    product_data = product_data.filter(product_status='inactive')
                else:
                    product_data=product_data

                if search_data:
                    product_data = product_data.filter(Q(product_name__icontains=search_data) | Q(product_brand__icontains=search_data))


            elif 'update' in request.POST:
                product_id = request.POST.get('product_id')
                product_desc = request.POST.get('description')
                product_stock = request.POST.get('product_stock')
                product_status = request.POST.get('product_status')
                product_obj = ProductModel.objects.get(product_id=int(product_id))
                product_obj.product_description = product_desc
                product_obj.seller_product_stock = product_stock
                product_obj.product_status  = product_status
                product_obj.save()
                return redirect('my_listing')

            elif 'delete' in request.POST:
                product_del = request.POST.get('product_del')
                pro_obj = ProductModel.objects.get(product_id=product_del)
                pro_obj.delete()
                return redirect('my_listing')


        return render(request,'listing_details.html',{'seller':seller_obj,'product_active':product_active,'product_inactive':product_inactive,'low_stock':low_stock,'no_stock':no_stock,
                                                                            'product_data':product_data,'category_data':category_data,'search_data':search_data,'category_select':category_select,'status_select':status_select})
    else:
        return redirect('seller_login')

def add_listing(request):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller=SellerDataModel.objects.get(seller_id=seller_id)

        if request.method=="POST":
            if 'pc_submit' in request.POST:
                cat_obj =ProductCategoryModel.objects.get(category_id=2)
                pc_name=request.POST.get('pc_name')
                pc_brand = request.POST.get('pc_brand')
                pc_description = request.POST.get('pc_description')
                pc_price = request.POST.get('pc_price')
                pc_stock = request.POST.get('pc_stock')
                pc_status = request.POST.get('pc_status')
                pc_ram = request.POST.get('pc_ram')
                pc_ram = int(pc_ram)*1000
                pc_storage = request.POST.get('pc_storage')
                pc_storage_unit = request.POST.get('pc_storage_unit')
                pc_storage = int(pc_storage)
                if pc_storage_unit=='GB':
                    pc_storage = pc_storage*1000
                else:
                    pc_storage = pc_storage*1000000
                pc_screen = request.POST.get('pc_screen')
                pc_processor = request.POST.get('pc_processor')
                pc_pro_gen = request.POST.get('pc_pro_gen')
                pc_pro_model = request.POST.get('pc_pro_model')
                processor_string = f"{pc_processor} {pc_pro_gen} {pc_pro_model}"
                pc_graphics = request.POST.get('pc_graphics')
                pc_res_x = request.POST.get('pc_resolution_x')
                pc_res_y = request.POST.get('pc_resolution_y')
                pc_refresh = request.POST.get('pc_refresh')
                pc_os = request.POST.get('pc_os')
                pc_warranty = request.POST.get('pc_warranty')
                pc_images = request.FILES.getlist('pc_images')
                pro_obj = ProductModel()
                pro_obj.seller = seller
                pro_obj.category = cat_obj
                pro_obj.product_name = pc_name
                pro_obj.product_brand =pc_brand
                pro_obj.product_description = pc_description
                pro_obj.product_price =pc_price
                pro_obj.seller_product_stock = pc_stock
                pro_obj.product_status = pc_status
                pro_obj.save()
                spec_obj = PCSpecificationModel()
                spec_obj.product = pro_obj
                spec_obj.category = cat_obj
                spec_obj.product_brand =pc_brand
                spec_obj.spec_ram = pc_ram
                spec_obj.spec_processor = processor_string
                spec_obj.spec_storage = pc_storage
                spec_obj.spec_gpu =pc_graphics
                spec_obj.spec_horizontal_resolution = pc_res_x
                spec_obj.spec_vertical_resolution = pc_res_y
                spec_obj.spec_display_size = pc_screen
                spec_obj.spec_os = pc_os
                spec_obj.spec_refresh_rate = pc_refresh
                spec_obj.warranty = pc_warranty
                spec_obj.product_status = pc_status
                spec_obj.save()
                for pc_image in pc_images:
                    pro_img = ProductImageModel()
                    pro_img.product = pro_obj
                    pro_img.product_image = pc_image
                    pro_img.save()

                return redirect('my_listing')
            elif 'lap_submit' in request.POST:
                cat_obj =ProductCategoryModel.objects.get(category_id=5)
                pc_name=request.POST.get('lap_name')
                pc_brand = request.POST.get('lap_brand')
                pc_description = request.POST.get('lap_description')
                pc_price = request.POST.get('lap_price')
                pc_stock = request.POST.get('lap_stock')
                pc_status = request.POST.get('lap_status')
                pc_ram = request.POST.get('lap_ram')
                pc_ram = int(pc_ram)*1000
                pc_storage = request.POST.get('lap_storage')
                pc_storage_unit = request.POST.get('lap_storage_unit')
                pc_storage = int(pc_storage)
                if pc_storage_unit=='GB':
                    pc_storage = pc_storage*1000
                else:
                    pc_storage = pc_storage*1000000
                pc_screen = request.POST.get('lap_screen')
                pc_processor = request.POST.get('lap_processor')
                pc_pro_gen = request.POST.get('lap_pro_gen')
                pc_pro_model = request.POST.get('lap_pro_model')
                processor_string = f"{pc_processor} {pc_pro_gen} {pc_pro_model}"
                pc_graphics = request.POST.get('lap_graphics')
                pc_res_x = request.POST.get('lap_resolution_x')
                pc_res_y = request.POST.get('lap_resolution_y')
                pc_refresh = request.POST.get('lap_refresh')
                pc_os = request.POST.get('lap_os')
                pc_warranty = request.POST.get('lap_warranty')
                lap_images = request.FILES.getlist('lap_images')
                pro_obj = ProductModel()
                pro_obj.seller = seller
                pro_obj.category = cat_obj
                pro_obj.product_name = pc_name
                pro_obj.product_brand =pc_brand
                pro_obj.product_description = pc_description
                pro_obj.product_price =pc_price
                pro_obj.seller_product_stock = pc_stock
                pro_obj.product_status = pc_status
                pro_obj.save()
                spec_obj = PCSpecificationModel()
                spec_obj.product = pro_obj
                spec_obj.category = cat_obj
                spec_obj.product_brand =pc_brand
                spec_obj.spec_ram = pc_ram
                spec_obj.spec_processor = processor_string
                spec_obj.spec_storage = pc_storage
                spec_obj.spec_gpu =pc_graphics
                spec_obj.spec_horizontal_resolution = pc_res_x
                spec_obj.spec_vertical_resolution = pc_res_y
                spec_obj.spec_display_size = pc_screen
                spec_obj.spec_os = pc_os
                spec_obj.spec_refresh_rate = pc_refresh
                spec_obj.warranty = pc_warranty
                spec_obj.product_status = pc_status
                spec_obj.save()
                for lap_image in lap_images:
                    pro_img = ProductImageModel()
                    pro_img.product = pro_obj
                    pro_img.product_image = lap_image
                    pro_img.save()

                return redirect('my_listing')

            elif 'phn-submit' in request.POST:
                cat_obj = ProductCategoryModel.objects.get(category_id=3)
                phn_name = request.POST.get('phn_name')
                phn_brand = request.POST.get('phn_brand')
                phn_description = request.POST.get('phn_description')
                phn_price = request.POST.get('phn_price')
                phn_stock = request.POST.get('phn_stock')
                phn_status = request.POST.get('phn_status')
                phn_ram = request.POST.get('phn_ram')
                phn_ram=int(phn_ram)*1000
                phn_storage = request.POST.get('phn_storage')
                phn_storage=int(phn_storage)*1000
                phn_color=request.POST.get('phn_color')
                pro_brand=request.POST.get('pro_brand')
                pro_gen=request.POST.get('pro-gen')
                phn_processor = f"{pro_brand} {pro_gen}"
                phn_resx = request.POST.get('phn-resx')
                phn_resy = request.POST.get('phn-resy')
                phn_battery = request.POST.get('phn-battery')
                phn_os = request.POST.get('phn-os')
                phn_screen =request.POST.get('phn-screen')
                phn_cam = request.POST.get('phn-cam')
                phn_warranty = request.POST.get('phn-warranty')
                phn_images =request.FILES.getlist('phn-images')
                pro_obj = ProductModel()
                pro_obj.seller = seller
                pro_obj.category = cat_obj
                pro_obj.product_name = phn_name
                pro_obj.product_brand = phn_brand
                pro_obj.product_description = phn_description
                pro_obj.product_price = phn_price
                pro_obj.seller_product_stock = phn_stock
                pro_obj.product_status = phn_status
                pro_obj.save()
                mob_spec_obj = SmartPhoneSpecificationModel()
                mob_spec_obj.product = pro_obj
                mob_spec_obj.category = cat_obj
                mob_spec_obj.product_brand = phn_brand
                mob_spec_obj.spec_ram = phn_ram
                mob_spec_obj.spec_storage = phn_storage
                mob_spec_obj.spec_processor = phn_processor
                mob_spec_obj.spec_horizontal_resolution = phn_resx
                mob_spec_obj.spec_vertical_resolution = phn_resy
                mob_spec_obj.color = phn_color
                mob_spec_obj.spec_battery = phn_battery
                mob_spec_obj.spec_display_size = phn_screen
                mob_spec_obj.spec_camera = phn_cam
                mob_spec_obj.spec_os = phn_os
                mob_spec_obj.warranty = phn_warranty
                mob_spec_obj.product_status = phn_status
                mob_spec_obj.save()
                for image in phn_images:
                    img_obj = ProductImageModel()
                    img_obj.product = pro_obj
                    img_obj.product_image = image
                    img_obj.save()

                return redirect('my_listing')

            elif 'tv-submit' in request.POST:
                cat_obj = ProductCategoryModel.objects.get(category_id=4)
                tv_name = request.POST.get('tv-name')
                tv_brand = request.POST.get('tv-brand')
                tv_description = request.POST.get('tv-description')
                tv_price = request.POST.get('tv-price')
                tv_stock = request.POST.get('tv-stock')
                tv_status = request.POST.get('tv-status')
                pro_obj = ProductModel()
                pro_obj.seller = seller
                pro_obj.category = cat_obj
                pro_obj.product_name = tv_name
                pro_obj.product_brand = tv_brand
                pro_obj.product_description = tv_description
                pro_obj.product_price = tv_price
                pro_obj.seller_product_stock = tv_stock
                pro_obj.product_status = tv_status
                pro_obj.save()
                tv_screen = request.POST.get('tv-screen')
                tv_res_x = request.POST.get('tv-res-x')
                tv_res_y = request.POST.get('tv-res-y')
                tv_os = request.POST.get('tv-os')
                tv_warranty = request.POST.get('tv-warranty')
                tv_obj = TeleVisionSpecificationModels()
                tv_obj.product = pro_obj
                tv_obj.category = cat_obj
                tv_obj.product_brand = tv_brand
                tv_obj.product_status = tv_status
                tv_obj.spec_display_size = tv_screen
                tv_obj.spec_horizontal_resolution = tv_res_x
                tv_obj.spec_vertical_resolution = tv_res_y
                tv_obj.spec_os = tv_os
                tv_obj.warranty = tv_warranty
                tv_obj.save()
                tv_images = request.FILES.getlist('tv-images')
                for image in tv_images:
                    img_obj = ProductImageModel()
                    img_obj.product = pro_obj
                    img_obj.product_image = image
                    img_obj.save()
                return redirect('my_listing')

            elif 'audio-submit' in request.POST:
                cat_obj = ProductCategoryModel.objects.get(category_id=1)
                a_name = request.POST.get('a-name')
                a_brand = request.POST.get('a-brand')
                a_description = request.POST.get('a-description')
                a_price = request.POST.get('a-price')
                a_stock = request.POST.get('a-stock')
                a_status = request.POST.get('a-status')
                pro_obj = ProductModel()
                pro_obj.seller = seller
                pro_obj.category = cat_obj
                pro_obj.product_name = a_name
                pro_obj.product_brand = a_brand
                pro_obj.product_description = a_description
                pro_obj.product_price = a_price
                pro_obj.seller_product_stock = a_stock
                pro_obj.product_status = a_status
                pro_obj.save()
                a_type = request.POST.get('a-type')
                a_bluetooth = request.POST.get('a-bluetooth')
                a_mic = request.POST.get('a-mic')
                a_playback = request.POST.get('a-playback')
                a_latency = request.POST.get('a-latency')
                a_warranty = request.POST.get('a-warranty')
                audio_obj = AudioSpecificationModel()
                audio_obj.product = pro_obj
                audio_obj.product_brand = a_brand
                audio_obj.category = cat_obj
                audio_obj.product_type = a_type
                audio_obj.spec_bluetooth = a_bluetooth
                audio_obj.spec_mic = a_mic
                audio_obj.spec_playback = a_playback
                audio_obj.spec_latency = a_latency
                audio_obj.warranty = a_warranty
                audio_obj.save()
                audio_images = request.FILES.getlist('a-images')
                for image in audio_images:
                    img_obj = ProductImageModel()
                    img_obj.product = pro_obj
                    img_obj.product_image = image
                    img_obj.save()
                return redirect('my_listing')


        return render(request, 'add_listing.html',{'seller':seller})
    else:
        return redirect('seller_login')

def add_discount(request):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller=SellerDataModel.objects.get(seller_id=seller_id)
        pro_data = ProductModel.objects.filter(seller=seller)
        event_data = EventModel.objects.filter(status='Active')
        discount_data = ProductDiscountModel.objects.filter(seller_id=seller)
        search_data = ''

        if request.method=='POST':
            if 'discount_submit' in request.POST:
                product_id = request.POST.get('product_name')
                event_id = request.POST.get('event_name')
                discount = request.POST.get('discount_amount')
                discount_obj = ProductDiscountModel()
                discount_obj.seller_id = seller
                discount_obj.product = ProductModel.objects.get(product_id=product_id)
                discount_obj.event = EventModel.objects.get(event_id=event_id)
                discount_obj.discount_amount = discount
                discount_obj.save()
                return redirect('add_discount')
            elif 'delete' in request.POST:
                discount_id = request.POST.get('discount_del')
                delete_obj = ProductDiscountModel.objects.get(discount_id=discount_id)
                delete_obj.delete()
                return redirect('add_discount')
            if 'search-btn' in request.POST:
                search_data = request.POST.get('search-data')
                discount_data = discount_data.filter(Q(product__product_name__icontains=search_data))

        return render(request,'seller_discount.html',{'seller':seller,'product_data':pro_data,'event_data':event_data,'discount_data':discount_data,'search_data':search_data})
    else:
        return redirect('seller_login')
def seller_registration(request):
    license_error = ''
    phone_error = ''
    email_error = ''
    gst_error = ''
    pan_error = ''
    if request.method == 'POST':
        s_license = request.POST.get('seller-lic')
        s_company_name = request.POST.get('company-name')
        s_phone = request.POST.get('seller-phn')
        s_address = request.POST.get('seller-address')
        s_email = request.POST.get('seller-mail')
        s_pan = request.POST.get('seller-pan')
        s_gst = request.POST.get('seller-gst')
        s_bank = request.POST.get('seller-bank')
        s_ifsc = request.POST.get('seller-ifsc')

        if SellerDataModel.objects.filter(seller_licence=s_license).exists():
            license_error = 'This licence already exists.'
        if SellerDataModel.objects.filter(seller_phone=s_phone).exists():
            phone_error = 'This Phone number already exists.'
        if SellerDataModel.objects.filter(seller_email=s_email).exists():
            email_error = 'This licence already exists.'
        if SellerDataModel.objects.filter(seller_gst=s_gst).exists():
            gst_error = 'This licence already exists.'
        if SellerDataModel.objects.filter(seller_pan=s_pan).exists():
            pan_error = 'This licence already exists.'

        if license_error or phone_error or email_error or gst_error or pan_error:
            return render(request,'sellerreg.html',{'licence':license_error,
                                                                          'phone':phone_error,
                                                                          'email':email_error,
                                                                           'gst':gst_error,
                                                                          'pan':pan_error})

        seller_obj = SellerDataModel()
        seller_obj.seller_licence = s_license
        seller_obj.seller_company_name = s_company_name
        seller_obj.seller_phone = s_phone
        seller_obj.seller_address = s_address
        seller_obj.seller_email = s_email
        seller_obj.seller_pan = s_pan
        seller_obj.seller_gst = s_gst
        seller_obj.seller_bank_acc = s_bank
        seller_obj.seller_IFSC = s_ifsc
        seller_obj.save()
        return redirect('seller_login')

    return render(request,'sellerreg.html')

def seller_login(request):
    email_error = ''
    otp_error =''
    show_content = False
    email_data = ''
    verified = False
    if request.method == 'POST':
        email_data = request.POST.get('seller-email')
        seller_data = SellerDataModel.objects.filter(seller_email=email_data)

        if 'verify-email'in request.POST:
            if seller_data.exists():
                show_content = True
                verified = True
                otp = send_otp(request)
                send_mail(
                    "Seller Login OTP",
                    f"Your OTP is:{otp} ",
                    "techbuy97@gmail.com",
                    [email_data],
                    fail_silently=False,
                )

            else:
                email_error="This Email doesn\'t Exists"

        elif 'submit-otp' in request.POST:
            submitted_otp = request.POST.get('otp-input')

            otp_key = request.session['otp_key']

            totp = pyotp.TOTP(otp_key,interval=300)
            if totp.verify(submitted_otp):
                seller_obj = SellerDataModel.objects.get(seller_email=email_data)
                request.session['seller_id'] = seller_obj.seller_id

                del request.session['otp_key']


                return redirect('seller_home')

            else:
                otp_error = 'Invalid OTP'
                show_content = True
                return render(request, 'selllogin.html',
                          {'show_content': show_content, 'email_data': email_data,
                           'email_error': email_error, 'otp_error': otp_error})

        return render(request, 'selllogin.html',{'show_content':show_content,'email_data':email_data,'email_error':email_error,'otp_error':otp_error,'verified':verified})
    else:
        return render(request,'selllogin.html')


def active_orders(request):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller=SellerDataModel.objects.get(seller_id=seller_id)
        order_data = OrderDetailsModel.objects.filter(product__seller=seller)
        orders_just_placed = 0
        for order in order_data:
            if order.status == 'dispatched':
                orders_just_placed += 1
        return render(request, 'activeorders.html', {'seller': seller, 'order_placed': orders_just_placed})
    else:
        return redirect('seller_login')

def returns(request):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller=SellerDataModel.objects.get(seller_id=seller_id)
        order_data = OrderDetailsModel.objects.filter(product__seller = seller)
        orders_cancelled= 0
        for order in order_data:
            if order.status == 'cancelled':
                orders_cancelled += 1
        return render(request,'returns.html',{'seller':seller,'order_cancelled':orders_cancelled })
    else:
        return redirect('seller_login')
def seller_logout(request):
    if 'seller_id' in request.session:
        del request.session['seller_id']
    return redirect('seller_login')
