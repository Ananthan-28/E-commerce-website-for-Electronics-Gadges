from django.shortcuts import render,redirect
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from AdminApp.models import ProductCategoryModel,EventModel
from UserApp.models import *
from SellerApp.models import *
from django.db.models import Sum
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def dashboard(request):
    active_users_count = int(UserDataModel.objects.filter(user_status='active').count())
    total_users = int(UserDataModel.objects.all().count())
    if total_users > 0:
        active_users_percentage = (active_users_count/total_users)*100
    else:
        active_users_percentage = 0

    active_merchants_count = int(SellerDataModel.objects.filter(seller_status='active').count())
    total_merchants = int(SellerDataModel.objects.all().count())
    if total_merchants > 0:
        active_merchants_percentage = (active_merchants_count/total_merchants)*100
    else:
        active_merchants_percentage = 0

    active_discounts = int(EventModel.objects.filter(status='Active').count())

    out_of_stock = int(ProductModel.objects.filter(seller_product_stock=0).count())

    latest_customers = UserDataModel.objects.order_by('-user_create_date')[:5]

    seller_sales = OrderDetailsModel.objects.values('product__seller').annotate(
        total_sales=Sum('user_order_quantity')).order_by('-total_sales')[:3]

    top_sellers = []
    for sale in seller_sales:
        seller = SellerDataModel.objects.get(seller_id=sale['product__seller'])
        top_sellers.append({
            'seller': seller.seller_company_name,
            'total_sales': sale['total_sales'],
        })

    pending_orders = int(OrderDetailsModel.objects.filter(payment_method='Cash on Delivery').count())
    cancelled_orders = int(OrderDetailsModel.objects.filter(status='cancelled').count())
    total_orders = int(OrderDetailsModel.objects.filter(status='dispatched').count())

    return render(request,'admin-dashboard.html',{'active_users':active_users_percentage,
                                                                       'active_users_count':active_users_count,
                                                                       'active_merchants':active_merchants_percentage,
                                                                       'active_merchants_count':active_merchants_count,
                                                                        'active_discounts':active_discounts,
                                                                        'out_of_stock':out_of_stock,
                                                                        'latest_customers':latest_customers,
                                                                        'top_sellers':top_sellers,
                                                                        'pending_orders':pending_orders,
                                                                        'cancelled_orders':cancelled_orders,
                                                                        'total_orders':total_orders})
def discounts(request):
    event_data = EventModel.objects.all()
    category_data = ProductCategoryModel.objects.all()
    event_data = event_data.order_by('-discount_start_date')
    if request.method =="POST":
        if 'add_event' in request.POST:
            event_name = request.POST.get('event_name')
            event_category = request.POST.get('event_category')
            cat_data=ProductCategoryModel.objects.get(category_id=int(event_category))
            event_img = request.FILES.get('event_img')
            discount_start_date = request.POST.get('discount_start_date')
            discount_end_date_str = request.POST.get('discount_end_date')
            discount_end_date_naive = parse_datetime(discount_end_date_str)
            discount_end_date = make_aware(discount_end_date_naive)
            event_status = request.POST.get('status')
            event_obj = EventModel()
            event_obj.event_name = event_name
            event_obj.event_category = cat_data
            event_obj.event_img = event_img
            event_obj.discount_start_date = discount_start_date
            event_obj.discount_end_date = discount_end_date
            event_obj.status = event_status
            event_obj.save()
            return redirect('admin_discounts')
        if 'edit_event' in request.POST:
            event_id = int(request.POST.get('event_id'))
            event_name = request.POST.get('event_name1')
            event_category = request.POST.get('event_category_hidden')
            cat_data = ProductCategoryModel.objects.get(category_name=event_category)
            event_img = request.FILES.get('event_img1')
            discount_start_date = request.POST.get('discount_start_date1')
            discount_end_date_str = request.POST.get('discount_end_date1')
            discount_end_date_naive = parse_datetime(discount_end_date_str)
            discount_end_date = make_aware(discount_end_date_naive)
            event_status = request.POST.get('status1')
            event_obj = EventModel.objects.get(event_id=event_id)
            event_obj.event_name = event_name
            event_obj.event_category = cat_data
            event_obj.event_img = event_img
            event_obj.discount_start_date = discount_start_date
            event_obj.discount_end_date = discount_end_date
            event_obj.status = event_status
            event_obj.save()
            return redirect('admin_discounts')

    return render(request, 'admin-event.html', {'event_data':event_data,'category_data':category_data})


def discount_remove(request,discount_id):
    event_obj = EventModel.objects.get(event_id=discount_id)
    event_obj.delete()
    return redirect('admin_discounts')

def categories(request):
    category_data = ProductCategoryModel.objects.all()
    if request.method == "POST":
        if 'cat_img' in request.FILES:
            cat_name = request.POST.get('cat_name')
            print(cat_name)
            cat_image = request.FILES.get('cat_img')
            print(cat_image)
            cat_obj = ProductCategoryModel()
            cat_obj.category_name = cat_name
            cat_obj.category_image = cat_image
            cat_obj.save()
            return redirect('admin_categories')
    return render(request,'admin_category.html',{'category_data':category_data})

def category_remove(request,cat_id):
    cat_obj = ProductCategoryModel.objects.get(category_id = cat_id)
    cat_obj.delete()
    return redirect('admin_categories')

def customers(request):
    customer_data = UserDataModel.objects.all()
    if request.method == "POST":
        search_data = request.POST.get('search_data')
        customer_data = customer_data.filter(Q(user_id__icontains=search_data) | Q(user_name__icontains=search_data) | Q(user_first_name__icontains=search_data) | Q(user_last_name__icontains=search_data) | Q(user_email__icontains = search_data) | Q(user_phone__icontains = search_data))

        return render(request, 'admin-customer.html', {'customer_data': customer_data})

    return render(request,'admin-customer.html',{'customer_data':customer_data})

def add_customer(request):
    if request.method == "POST":
        user_obj = UserDataModel()
        user_name = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        user_phn = request.POST.get('user_phn')
        user_mail = request.POST.get('user_email')
        user_obj.user_name = user_name
        user_obj.user_first_name = first_name
        user_obj.user_last_name = last_name
        user_obj.user_password = password
        user_obj.user_phone = user_phn
        user_obj.user_email = user_mail
        user_obj.save()

        return redirect('admin_customers')

def delete_customer(request,delete_id):
    user_obj = UserDataModel.objects.get(user_id=delete_id)
    user_obj.delete()
    return redirect('admin_customers')

def customer_details(request,customer_id):
    user_obj = UserDataModel.objects.get(user_id = customer_id)
    order_data = OrderDetailsModel.objects.filter(user=user_obj)
    order_count = order_data.count()
    review_data = ReviewDataModel.objects.filter(user = user_obj)
    review_count = review_data.count()
    half_rating = False
    star_range = range(5)
    for i in review_data:
        if i.user_rating is None:
            i.user_rating = 0
            i.half_rating = False
        elif 2.5 <= ((i.user_rating * 10) % 10) <= 5:
            i.half_rating = True
            i.user_rating = int(i.user_rating)
        else:
            i.half_rating = False


    if request.method == "POST":
        if 'profile_upd' in request.FILES:
            profile_pic = request.FILES.get("profile_upd")
            user_obj.user_profile_img = profile_pic
            user_obj.save()
        elif 'username_btn' in request.POST:
            username = request.POST.get('username')
            user_obj.user_name = username
            user_obj.save()
        elif 'name_btn' in request.POST:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            user_obj.user_first_name = firstname
            user_obj.user_last_name = lastname
            user_obj.save()
        elif 'email_btn' in request.POST:
            email = request.POST.get('email')
            user_obj.user_email = email
            user_obj.save()
        elif 'phnobtn' in request.POST:
            phno = request.POST.get('phno')
            user_obj.user_phone = phno
            user_obj.save()
        elif 'deactivate_btn' in request.POST:
            user_obj.user_status = 'inactive'
            user_obj.save()
        elif 'activate_btn' in request.POST:
            user_obj.user_status = 'active'
            user_obj.save()

        return redirect('customer_details',customer_id=customer_id)

    return render(request,'admin-customer-details.html',{'user_obj':user_obj,'order_data':order_data,'order_count':order_count,'review_data':review_data,'review_count':review_count,'half_rating':half_rating,'star_range':star_range})

def sellers(request):
    seller_data = SellerDataModel.objects.annotate(product_count=Count('productmodel'))
    if request.method == "POST":
        search_data = request.POST.get('search_data')
        seller_data = seller_data.filter(Q(seller_id__icontains=search_data) | Q(seller_company_name__icontains=search_data) | Q(seller_licence__icontains=search_data)  | Q(seller_email__icontains = search_data) | Q(seller_phone__icontains = search_data))

        return render(request, 'admin-sellers.html', {'seller_data': seller_data})

    return render(request,'admin-sellers.html', {'seller_data': seller_data})

def add_seller(request):
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
            return render(request, 'sellerreg.html', {'licence': license_error,
                                                      'phone': phone_error,
                                                      'email': email_error,
                                                      'gst': gst_error,
                                                      'pan': pan_error})

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

        return redirect('admin_sellers')



def delete_seller(request,delete_id):
    seller_obj = SellerDataModel.objects.get(seller_id=delete_id)
    seller_obj.delete()
    return redirect('admin_sellers')

def seller_details(request,vendor_id):
    seller_obj = SellerDataModel.objects.get(seller_id = vendor_id)
    product_data = ProductModel.objects.filter(seller = seller_obj)
    product_count = product_data.count()
    if request.method == "POST":
        if 'deactivate_btn' in request.POST:
            seller_obj.seller_status = 'inactive'
            seller_obj.save()
        elif 'activate_btn' in request.POST:
            seller_obj.seller_status = 'active'
            seller_obj.save()

        return redirect('vendor_details',vendor_id=vendor_id)

    return render(request,'admin-seller-details.html',{'seller_obj':seller_obj,'product_data':product_data,'product_count':product_count})

def products(request):
    product_data = ProductModel.objects.all()
    paginator_data = Paginator(product_data,15)
    page = request.GET.get('page')
    try:
        load_page = paginator_data.page(page)
    except PageNotAnInteger:
        load_page = paginator_data.page(1)
    except EmptyPage:
        load_page = paginator_data.page(paginator_data.num_pages)
    if request.method == "POST":
        if 'deactivate_btn' in request.POST:
            product_id = request.POST.get('product_id')
            pro_obj = ProductModel.objects.get(product_id=product_id)
            pro_obj.product_status = 'inactive'
            pro_obj.save()
        elif 'activate_btn' in request.POST:
            product_id = request.POST.get('product_id')
            pro_obj = ProductModel.objects.get(product_id=product_id)
            pro_obj.product_status = 'active'
            pro_obj.save()

        return redirect('admin_products')

    return render(request,'admin-products.html',{'load_page':load_page})

def remove_product(request,product_id):
    product_obj = ProductModel.objects.get(product_id=product_id)
    product_obj.delete()
    return redirect('admin_products')

def orders(request):
    order_data = OrderDetailsModel.objects.all()
    if request.method == "POST":
        search_data = request.POST.get('search_data')
        order_data = order_data.filter(
            Q(user_order_id__icontains=search_data) | Q(product__product_name__icontains=search_data) | Q(
                user__user_name__icontains=search_data) | Q(product__seller__seller_company_name__icontains=search_data))

        return render(request, 'admin-orders.html', {'order_data': order_data})

    return render(request,'admin-orders.html',{'order_data':order_data})

def order_details(request,order_id):
    order_obj = OrderDetailsModel.objects.get(user_order_id=order_id)
    return render(request,'admin-order-details.html',{'order_obj':order_obj})
