from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AdminDataModel)
admin.site.register(ProductCategoryModel)
admin.site.register(EventModel)
admin.site.register(ProductBrandModel)

