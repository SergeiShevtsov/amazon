from django.contrib import admin
from .models import Product, Manager, Brand, TypeOfProduct, Message, ACOS, Category
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
		exclude = ('changes', 'positions_by_keys', 'offers', 'event', 'link_to_seo', '')

# class ProductResource(resources.ModelResource):
# 	brand = fields.Field(column_name='brand', attribute='brand', widget=ForeignKeyWidget(Brand, 'brand'))
# 	manager=fields.Field(column_name='manager', attribute='manager', widget=ForeignKeyWidget(Manager, 'username'))
# 	type = fields.Field(column_name='type', attribute='type', widget=ForeignKeyWidget(TypeOfProduct, 'type'))
# 	product_name = fields.Field(column_name='Product Short Name', attribute='product_name')
# 	date = fields.Field(column_name='Yesterday\'s Date on Marketplace', attribute='sales')
# 	sales = fields.Field(column_name='my sales', attribute='sales')
# 	# category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(ProductCategory,'name'))
# 	class Meta:
# 		fields = ('product_name', 'asin', 'link', 'conversion_rate', 'rating', 'date', 'sales', 'sel_acc', 'brand', 'manager', 'type')
# 		model = Product
# 		export_order = ('product_name', 'asin', 'link', 'conversion_rate', 'rating', 'date', 'sales', 'sel_acc', 'brand', 'manager', 'type')
	

class ProductAdmin(ImportExportModelAdmin):
	resources_class = ProductResource
	list_display=["product_name", "id", "date", 'sales', 'price', 'bsr', 'brand', 'manager'] # field.name for field in Product._meta.fields
	search_fields = ('product_name',)

admin.site.register(Product, ProductAdmin)

@admin.register(Brand)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'brand')

@admin.register(Message)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id','product_type', 'text', 'user',)
	
@admin.register(ACOS)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id','product_name', 'spend', 'sale', 'date')


@admin.register(TypeOfProduct)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "type", 'brand',  "manager", "status", 'owner', 'category',)


@admin.register(Manager)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', "user", 'username')


class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username')


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'category',)

# Register your models here.
