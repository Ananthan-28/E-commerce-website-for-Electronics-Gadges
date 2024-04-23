from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SellerDataModel)
admin.site.register(ProductModel)
admin.site.register(ProductImageModel)
admin.site.register(PCSpecificationModel)
admin.site.register(SmartPhoneSpecificationModel)
admin.site.register(TeleVisionSpecificationModels)
admin.site.register(AudioSpecificationModel)
admin.site.register(ProductDiscountModel)

