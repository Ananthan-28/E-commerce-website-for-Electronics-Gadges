from django.db import models
from django.utils import timezone
from AdminApp.models import *
from django.core.validators import MaxValueValidator, MinValueValidator


class SellerDataModel(models.Model):
    seller_id = models.AutoField(primary_key=True)
    seller_licence = models.CharField(max_length=255,unique=True)
    seller_company_name = models.CharField(max_length=50)
    seller_phone = models.CharField(max_length=15,unique=True)
    seller_address = models.TextField(max_length=255)
    seller_email = models.CharField(max_length=100,unique=True)
    seller_pan = models.CharField(max_length=20,unique=True)
    seller_gst = models.CharField(max_length=50,unique=True)
    seller_bank_acc = models.CharField(max_length=50)
    seller_IFSC = models.CharField(max_length=50)
    seller_status = models.CharField(max_length=8, default='active')

    class Meta:
        db_table = 'Seller_data_model'

    def __str__(self):
        return self.seller_company_name

class ProductModel(models.Model):
    product_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(SellerDataModel, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=500)
    product_description = models.CharField(max_length=500)
    product_price = models.IntegerField()
    seller_product_stock = models.IntegerField()
    user_rating = models.DecimalField(max_digits=2, decimal_places=1,validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    product_brand = models.ForeignKey(ProductBrandModel,on_delete=models.CASCADE,null=True)
    product_status = models.CharField(max_length=8, default='active')

    class Meta:
        db_table = 'Product_model'

    def __str__(self):
        return self.product_name

    def latest_discount(self):
        latest_discount = self.productdiscounts.all().order_by('-created_at').first()
        return latest_discount

    def has_discount(self):
        latest_discount = self.latest_discount()
        if latest_discount is not None and latest_discount.event.status == 'Active' and latest_discount.event.discount_end_date > timezone.now():
            return self.productdiscounts.exists()
        else:
            return False

    def discount_price(self):
        latest_discount = self.latest_discount()

        if latest_discount is not None and latest_discount.event.status == 'Active' and latest_discount.event.discount_end_date > timezone.now():
            discounted_price = self.product_price - latest_discount.discount_amount
            return discounted_price
        else:
            return self.product_price

    def discount_percentage(self):
        latest_discount = self.latest_discount()
        if latest_discount is not None:
            return round(((latest_discount.discount_amount/self.product_price)*100),1)
        else:
            return 0

def upload_to_path(instance, filename):
    product_type = instance.product.category.category_name.lower()
    return f'product_images/{product_type}/{filename}'
class ProductImageModel(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel,related_name= 'images' ,on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to=upload_to_path)

    class Meta:
        db_table = 'product_image_model'

    def __str__(self):
        return self.product.product_name

class PCSpecificationModel(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, related_name="computer", on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    product_brand = models.CharField(max_length=15)
    spec_ram = models.IntegerField()
    spec_processor = models.CharField(max_length=50)
    spec_storage = models.IntegerField()
    spec_gpu = models.CharField(max_length=50,null=True)
    spec_horizontal_resolution = models.IntegerField()
    spec_vertical_resolution = models.IntegerField(null=True)
    spec_display_size = models.DecimalField(max_digits=4,decimal_places=1)
    spec_os = models.CharField(max_length=10)
    spec_refresh_rate = models.IntegerField()

    warranty = models.IntegerField()
    product_status = models.CharField(max_length=8, default='active')

    class Meta:
        db_table = 'pc_spec_model'

    def __str__(self):
        return self.product.product_name

class SmartPhoneSpecificationModel(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, related_name='phone', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    product_brand = models.CharField(max_length=15)
    spec_ram = models.IntegerField()
    spec_processor = models.CharField(max_length=50)
    spec_storage = models.IntegerField()
    spec_horizontal_resolution = models.IntegerField()
    spec_vertical_resolution = models.IntegerField(null=True)
    spec_display_size = models.DecimalField(max_digits=4,decimal_places=1)
    color = models.CharField(max_length=10)
    spec_battery = models.IntegerField()
    spec_camera = models.IntegerField()
    spec_os = models.CharField(max_length=10)

    warranty = models.IntegerField()
    product_status = models.CharField(max_length=8, default='active')

    class Meta:
        db_table = 'smartphone_spec_model'

    def __str__(self):
        return self.product.product_name

class TeleVisionSpecificationModels(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel,related_name='television', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    product_brand = models.CharField(max_length=15)
    spec_horizontal_resolution = models.IntegerField()
    spec_vertical_resolution = models.IntegerField(null=True)
    spec_display_size = models.DecimalField(max_digits=4,decimal_places=1)
    spec_os = models.CharField(max_length=10)

    warranty = models.IntegerField()
    product_status = models.CharField(max_length=8, default='active')

    class Meta:
        db_table = 'Television_spec_model'

    def __str__(self):
        return self.product.product_name

class AudioSpecificationModel(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, related_name='audio', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    product_brand = models.CharField(max_length=15)
    product_type = models.TextField(max_length=50)
    spec_bluetooth = models.DecimalField(max_digits=2,decimal_places=1)
    spec_playback = models.IntegerField()
    spec_mic = models.CharField(max_length=5)
    spec_latency = models.IntegerField()

    warranty = models.IntegerField()
    product_status = models.CharField(max_length=8, default='active')

    class Meta:
        db_table = 'audio_spec_model'

    def __str__(self):
        return self.product.product_name

class ProductDiscountModel(models.Model):
    discount_id = models.AutoField(primary_key=True)
    seller_id = models.ForeignKey(SellerDataModel, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='productdiscounts')
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    discount_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_discount_model'

    def __str__(self):
        return self.product.product_name



