from django.contrib import admin
from .models import Product, Manager, Brand, TypeOfProduct
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import ForeignKeyWidget

admin.site.register(Brand)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("product_name", "id", "date", 'reviews', 'sales', 'price', 'bsr', 'brand', 'manager', 'link')
	search_fields = ('product_name',)

@admin.register(TypeOfProduct)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "type", 'brand',  "manager")
	
@admin.register(Manager)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "user", 'username')

class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username')



# Register your models here.
