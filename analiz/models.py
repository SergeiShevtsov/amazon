from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class ACOS(models.Model):
	product_name = models.ForeignKey('TypeOfProduct', on_delete=models.CASCADE)
	acos = models.DecimalField(max_digits=2, decimal_places=0)
	spend = models.IntegerField()
	sale = models.IntegerField()
	budget = models.IntegerField()
	date = models.CharField(max_length=50)
	
	
class Message(models.Model):
	text = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product_type = models.ForeignKey('TypeOfProduct', on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)
	
	def __str__(self, ):
		return self.text


class Product(models.Model):
	asin = models.CharField(max_length=15, blank=True, null = True) 
	product_name = models.CharField(max_length=30) 
	date = models.DateField() 
	sales = models.IntegerField()
	price = models.DecimalField(max_digits=4, decimal_places=2)
	bsr = models.IntegerField(blank=True, null = True)
	rating = models.DecimalField(max_digits=2, decimal_places=1)
	
	link = models.URLField(blank=True, null = True)
	changes = models.TextField(blank=True, null = True)
	positions_by_keys = models.CharField(max_length=400, blank=True, null = True)
	conversion_rate = models.CharField(max_length=10, null = True, blank = True)
	offers = models.TextField(blank=True, null = True)
	event = models.TextField(max_length=1000 ,blank=True, null = True)
	link_to_seo = models.URLField(blank=True, null = True)
	fba_inventory = models.TextField(blank=True, null = True) # add 
	sel_acc = models.TextField(blank=True, null = True) 
	reviews = models.IntegerField(blank=True, null = True)
	
	brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
	manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
	type = models.ForeignKey('TypeOfProduct', on_delete=models.CASCADE)


	class Meta:
		ordering = ['date',]
	
	def __str__(self):
		return self.product_name


class TypeOfProduct(models.Model): # конкретно все товары
	type = models.CharField(max_length=30, unique=True)
	manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
	category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
	brand = models.ForeignKey('Brand', on_delete=models.CASCADE,)
	status_min = models.IntegerField(default=25) # убрал null & blank
	status_need = models.IntegerField(default=101) # убрал null & blank
	
	ostatki = models.PositiveIntegerField(blank=True, null = True) # удалить
	owner = models.CharField(max_length=40, blank=True, null = True)
	BAN = 'BAN'
	OUT_OF_STOCK = 'OOS'
	SUPRESSION = 'SSS'
	IN_DEV = "InDev"
	IS_S = 'IsS'
	ANOTHER_ISSUE = 'AN_ISS'
	STATUS_CHOICES = [
		(IN_DEV, 'В разработке'),
		(IS_S, 'Продается'),
		(ANOTHER_ISSUE, 'Другая причина'),
		(BAN, 'Бан'),
		(OUT_OF_STOCK, 'Нет на складе'),
		(SUPRESSION, 'Ограничение'),
	]
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IS_S)
	
	class Meta:
		ordering = ['type',]
	def __str__(self):
		return self.type
	
	
# можно убрать или сделать брэндом
class Brand(models.Model):
	brand = models.CharField(max_length=20, unique=True)
	def __str__(self):
		return self.brand
	class Meta:
		ordering = ['brand',]
	
	
class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default='1')
	username = models.CharField(max_length=20, unique=True)
	image = models.ImageField(upload_to='images/', null = True, blank = True)
	
	def __str__(self):
		return self.username
	
	class Meta:
		ordering = ['username',]


class Category(models.Model):
	category = models.CharField(max_length=20, unique=True)
	
	def __str__(self):
		return self.category
	
	class Meta:
		ordering = ['category',]

# Create your models here.