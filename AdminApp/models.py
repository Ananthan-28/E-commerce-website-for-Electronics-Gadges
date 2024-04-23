from django.db import models


# Create your models here.
class AdminDataModel(models.Model):
    adm_ID = models.AutoField(primary_key=True)
    adm_username = models.CharField(max_length=20,unique=True)
    adm_password = models.CharField(max_length=20)
    adm_email = models.CharField(max_length=50,unique=True)
    adm_phone = models.CharField(max_length=15,unique=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_data_model'

    def __str__(self):
        return self.adm_username


class ProductCategoryModel(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    category_image = models.ImageField(upload_to='categories',null=True)

    class Meta:
        db_table = 'product_category_model'

    def __str__(self):
        return self.category_name

def upload_to(instance, filename):
    category_name = instance.category.category_name.lower()
    return f'brand_images/{category_name}/{filename}'

class ProductBrandModel(models.Model):
    brand_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(ProductCategoryModel,on_delete=models.CASCADE)
    brand_name = models.TextField(max_length=20)
    brand_image = models.ImageField(upload_to=upload_to)

    class Meta:
        db_table = 'Brand Model'

    def __str__(self):
        return self.brand_name

class EventModel(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    event_category = models.ForeignKey(ProductCategoryModel,on_delete=models.CASCADE,null=True)
    event_img = models.ImageField(upload_to='events')
    discount_start_date = models.DateTimeField(auto_now_add=True)
    discount_end_date = models.DateTimeField()
    status = models.CharField(max_length=8,default='Active')

    class Meta:
        db_table = 'event_model'

    def __str__(self):
        return self.event_name





