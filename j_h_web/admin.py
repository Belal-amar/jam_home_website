from django.contrib import admin
from .models import Product, User ,Category,Order,Orderitem
admin.site.register (Product)
admin.site.register (User)
admin.site.register (Category)
admin.site.register (Orderitem)
admin.site.register (Order)