from django.db import models
from SellerApp.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class UserDataModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50,unique=True)
    user_first_name = models.CharField(max_length=50,null=True)
    user_last_name = models.CharField(max_length=50,null=True)
    user_password = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=15,unique=True)
    user_email = models.EmailField(max_length=100,unique=True)
    user_profile_img = models.ImageField(upload_to='profile_pic/',null=True)
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_status = models.CharField(max_length=8, default='active')

    class Meta:
        db_table = 'user_data_model'

    def __str__(self):
        return self.user_name

class UserAddressDataModel(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    address_name=models.TextField(max_length=50, null=True)
    house_address = models.CharField(max_length=100)
    city_address = models.TextField(max_length=50)
    state_address = models.TextField(max_length=50)
    pincode_address = models.CharField(max_length=6)
    phone_no = models.CharField(max_length=10,null=True)

    class Meta:
        db_table = 'user_address_model'

    def __str__(self):
        return self.user.user_name


class CartDataModel(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_data_model'

    def total_price(self):
        if self.product.has_discount():
            discounted_price = self.product.discount_price()
            return self.cart_quantity * discounted_price
        else:
            return self.cart_quantity * self.product.product_price

    def real_price(self):
        return self.cart_quantity * self.product.product_price


    def __str__(self):
        return self.user.user_name

class ReviewDataModel(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    user_review = models.CharField(max_length=255,null=True)
    user_rating = models.DecimalField(max_digits=2, decimal_places=1 , validators=[MinValueValidator(0),MaxValueValidator(5)],null=True)
    review_date = models.DateField(auto_now_add=True,null=True)

    class Meta:
        db_table = 'review_model'

    def __str__(self):
        return self.product.product_name


class OrderDetailsModel(models.Model):
    user_order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddressDataModel, on_delete=models.CASCADE)
    user_order_quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    billing_ref_no = models.IntegerField(unique=True)
    order_cost = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=20,null=True)
    status = models.TextField(max_length=10,default='dispatched')

    class Meta:
        db_table = 'order_details_model'

    def __str__(self):
        return self.user.user_name


class WishlistModel(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist_model'

    def __str__(self):
        return self.user.user_name

