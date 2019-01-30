from django.contrib import admin

from .models import (
    MenuItem,
    Pizza,
    Extra,
    Order,
    OrderItem
)


# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Pizza)
admin.site.register(Extra)
admin.site.register(Order)
admin.site.register(OrderItem)
