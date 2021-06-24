from django.contrib import admin
from .models import Product, Manager, Brand, TypeOfProduct
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import ForeignKeyWidget



class ProductResource(resources.ModelResource):
	brand = fields.Field(column_name='brand', attribute='brand', widget=ForeignKeyWidget(Brand,'brand'))
	manager=fields.Field(column_name='manager', attribute='manager', widget=ForeignKeyWidget(Manager,'username'))
	type = fields.Field(column_name='type', attribute='type', widget=ForeignKeyWidget(TypeOfProduct,'type'))
	
	# category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(ProductCategory,'name'))
	class Meta:
		model = Product
	

class ProductAdmin(ImportExportModelAdmin):
	resources_class = ProductResource
	list_display=[field.name for field in Product._meta.fields if field.name != 'id']

admin.site.register(Product, ProductAdmin)

@admin.register(Brand)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'brand')


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
# 	list_display = ("product_name", "id", "date", 'reviews', 'sales', 'price', 'bsr', 'brand', 'manager', 'link')
# 	search_fields = ('product_name',)

@admin.register(TypeOfProduct)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "type", 'brand',  "manager")
	
@admin.register(Manager)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "user", 'username')

class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username')



# Register your models here.
