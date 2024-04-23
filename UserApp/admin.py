from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserDataModel)
admin.site.register(UserAddressDataModel)
admin.site.register(CartDataModel)
admin.site.register(ReviewDataModel)
admin.site.register(OrderDetailsModel)
admin.site.register(WishlistModel)


