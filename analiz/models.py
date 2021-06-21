from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image



class Product(models.Model):
	product_name = models.CharField(max_length=30) #Title
	asin = models.CharField(max_length=15, blank=True, null = True) 
	link = models.URLField(blank=True, null = True)
	changes = models.TextField(blank=True, null = True)
	positions_by_keys = models.CharField(max_length=400, blank=True, null = True)
	price = models.DecimalField(max_digits=4, decimal_places=2)
	bsr = models.IntegerField(blank=True, null = True)
	sales = models.IntegerField()
	conversion_rate = models.CharField(max_length=10, null = True, blank = True) 
	rating = models.DecimalField(max_digits=2, decimal_places=1)
	offers = models.TextField(blank=True, null = True)
	date = models.DateField() #auto_now=True,
	event = models.TextField(blank=True, null = True) 
	reviews = models.IntegerField(blank=True, null = True)
	brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
	manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
	type = models.ForeignKey('TypeOfProduct', on_delete=models.CASCADE)
	reviews = models.IntegerField(blank=True, null = True)
	link_to_seo = models.URLField(blank=True, null = True)
	sel_acc = models.TextField(blank=True, null = True) 
	class Meta:
		ordering = ['date',]
	
	def __str__(self):
		return self.product_name


class TypeOfProduct(models.Model): # конкретно все товары
	type = models.CharField(max_length=30, unique=True)
	manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
	brand = models.ForeignKey('Brand', on_delete=models.CASCADE,)
	
	def __str__(self):
		return self.type
	
	
# можно убрать или сделать брэндом
class Brand(models.Model):
	brand = models.CharField(max_length=20, unique=True)
	def __str__(self):
		return self.brand
	
	
class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default='1')
	username = models.CharField(max_length=20, unique=True)
	image = models.ImageField(upload_to='images/', null = True, blank = True)
	def __str__(self):
		return self.username


# Create your models here.