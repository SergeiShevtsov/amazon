from django.contrib import admin
from .models import Product, Manager, Brand, TypeOfProduct
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

admin.site.register(Brand)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("product_name", "id", "date", 'manager')

@admin.register(TypeOfProduct)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "type", 'brand',  "manager")
	
@admin.register(Manager)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "user", 'username')

# Register your models here.
