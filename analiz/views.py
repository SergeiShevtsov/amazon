from .models import Product, Manager, Brand, TypeOfProduct
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Avg
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import DateForm, AddProduct, AddNewProduct, AddTypeOfProduct, ChooseType
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
import itertools
from django.db.models.functions import ExtractMonth, TruncMonth
from django.utils import timezone
from django.template import Context, loader
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect


def akcii(request):
	type = TypeOfProduct.objects.all().order_by('manager')
	products = Product.objects.all()
	total_sales = []
	ave_sales = []
	got_money = []
	date1 = '2020-01-01'
	date2 = datetime.now()
	form = DateForm(request.POST or None)
	if form.is_valid():
		date1 = form.clean_date1()
		date2 = form.clean_date2()
		if date1==None or date2==None:
			date1 = '2020-01-01'
			date2 = datetime.now()
		products = products.filter(date__gte=date1).filter(date__lte=date2)
	if products.count() == 0:
		products = Product.objects.all()
	for item in type:
		name = item.type
		type_sales = 0
		average_sales = 0
		coun = 0
		money = 0
		for p in products:
			if name == p.product_name:
				coun += 1
				s = p.sales
				price = p.price
				money += price*s
				type_sales += s
				average_sales += s
		if coun == 0:
			coun = 1
		average_sales = average_sales / coun
		average_sales = round(average_sales,0)
		ave_sales.append(average_sales)
		total_sales.append(type_sales)
		got_money.append(money)
	
	

	context = {'sales':total_sales, 'money':got_money, 'type':type, 'form':form}
	return render(request, 'akcii.html', context)


@csrf_exempt
def new_page(request, *type_of):
	managers = Manager.objects.all()
	type = TypeOfProduct.objects.all().order_by('manager')
	prod = Product.objects.last()
	new_product = AddNewProduct(request.POST or None, instance=prod)
	new_type = AddTypeOfProduct(request.POST or None)
	choose_type = ChooseType(request.POST or None)
	products = ''
	if request.method == 'POST' and new_product.is_valid():
		new_product.save()	
	elif request.method == 'POST' and new_type.is_valid():
		new_type.save()
	elif choose_type.is_valid() and request.method == "POST":
		data = choose_type.clean_type()
		prod = Product.objects.filter(type=data).last()
		new_product = AddNewProduct(request.POST or None, instance=prod)
	else:
		new_product = AddNewProduct(request.POST or None, instance=prod)
		new_type = AddTypeOfProduct(request.POST or None)
	
	
	context = {'new_product':new_product, 'new_type':new_type, 'choose':choose_type, 'prod':products}
	return render(request, 'New.html', context)


def motivation(request):
	managers = Manager.objects.all()
	type = TypeOfProduct.objects.all().order_by('manager')
	product = Product.objects.exclude(changes='бан')
	
	date1 = '2020-01-01'
	date2 = datetime.now()
	form = DateForm(request.POST or None)
	if form.is_valid():
		date1 = form.clean_date1()
		date2 = form.clean_date2()
		if date1==None or date2==None:
			date1 = '2020-01-01'
			date2 = datetime.now()
		product = product.filter(date__gte=date1).filter(date__lte=date2)
	if product.count() == 0:
		product = Product.objects.all()
	
	total_sales = []
	ave_sales = []
	for item in type:
		name = item.type
		type_sales = 0
		average_sales = 0
		coun = 0
		for p in product:
			if name == p.product_name:
				coun += 1
				s = p.sales
				price = p.price
				type_sales += s
				average_sales += s
		if coun == 0:
			coun = 1
		average_sales = average_sales / coun
		average_sales = round(average_sales,0)
		ave_sales.append(average_sales)
		total_sales.append(type_sales)
	dictionary = dict(zip(type, ave_sales))
	
	context = {'managers':managers, 'type':type, 'product':product, 'sales':total_sales, 'dicti':dictionary, 'form':form}
	return render(request, 'motivation.html', context)
	

def registerPage(request): 
	if request.method == 'POST':
		form = createUserForm(request.POST)
		profile_form = profileForm(request.POST)   
	else:
		form = createUserForm(request.GET)
		profile_form = profileForm(request.GET)
	context = {'form': form, 'profile_form': profile_form}
	return render(request, 'register.html', context)

@csrf_exempt
def mypage(request, manager_id):
	text_alarm = ''
	managers = Manager.objects.all()
	product = Product.objects.all().filter(manager=(manager_id))
	date1 = '2020-01-01'
	date2 = datetime.now()
	form = DateForm(request.POST or None)
	if form.is_valid():
		date1 = form.clean_date1()
		date2 = form.clean_date2()
		if date1==None or date2==None:
			date1 = '2020-01-01'
			date2 = datetime.now()
		product = product.filter(date__gte=date1).filter(date__lte=date2)
	if product.count() == 0:
		product = Product.objects.all()
		text_alarm = 'Данных по продуктам за данный период не обнаружено'


	type = TypeOfProduct.objects.all().filter(manager=manager_id)
	type_for_graphi = TypeOfProduct.objects.all().order_by('manager')
	if type.count() == 0:
		type = TypeOfProduct.objects.all()
	maxim_list = []
	for i in type:
		if i.owner == "max" or i.owner == "Max":
			maxim_list.append(i)
		else:
			pass

	brands = Brand.objects.all() 
	monthes = Product.objects.filter(manager=manager_id).values('product_name', 'sales', 'date').annotate(month=TruncMonth('date')).annotate(sales_by_month=Sum('sales'))
	
	max_total_sales = []
	max_ave_sales = []
	max_got_money = []
	
	total_sales = []
	ave_sales = []
	got_money = []
	for item in type:
		name = item.type
		type_sales = 0
		average_sales = 0
		coun = 0
		money = 0
		for p in product:
			if name == p.product_name:
				coun += 1
				s = p.sales
				price = p.price
				money += price*s
				type_sales += s
				average_sales += s
		if coun == 0:
			coun = 1
		average_sales = average_sales / coun
		average_sales = round(average_sales,0)
		ave_sales.append(average_sales)
		total_sales.append(type_sales)
		got_money.append(money)
		
		if item.owner == 'Max' or item.owner == 'max':
			max_ave_sales.append(average_sales)
			max_total_sales.append(type_sales)
			max_got_money.append(money)
	
	
	return render(request, 'MyPage.html', {'form':form, 'product' : product, 'managers' : managers, 'type' : type, 'monthes': monthes, 'type_1':total_sales,'ave_sales':ave_sales , 'brands':brands, 'manage_id' : manager_id, 'money':got_money, 'maxim':maxim_list, 'max_total_sales':max_total_sales, 'max_ave_sales':max_ave_sales, 'max_got_money':max_got_money})


def brand(request, manager_id, brandname=0):
	brands = Brand.objects.all()
	managers = Manager.objects.all()
	type = TypeOfProduct.objects.all().filter(brand=brandname)
	product = Product.objects.all().filter(brand=brandname)
	

	date1 = '2020-01-01'
	date2 = datetime.now()
	form = DateForm(request.POST or None)
	if form.is_valid():
		date1 = form.clean_date1()
		date2 = form.clean_date2()
		if date1==None or date2==None:
			date1 = '2020-01-01'
			date2 = datetime.now()
		product = product.filter(date__gte=date1).filter(date__lte=date2)
	if product.count() == 0:
		product = Product.objects.all()
	
	total_sales = []
	ave_sales = []
	for item in type:
		name = item.type
		type_sales = 0
		average_sales = 0
		coun = 0
		for p in product:
			if name == p.product_name:
				coun += 1
				s = p.sales
				type_sales += s
				average_sales += s
		if coun == 0:
			coun = 1
		average_sales = average_sales / coun
		ave_sales.append(average_sales)
		total_sales.append(type_sales)
	
	return render(request, 'MyPage.html', {'form':form, 'product' : product, 'managers' : managers, 'type' : type, 'type_1':total_sales,'ave_sales':ave_sales , 'brands':brands, 'manage_id' : manager_id})



def manager_view(request, manager_id=1):
	managers = Manager.objects.all()
	product = Product.objects.all()
	type = TypeOfProduct.objects.all()
	brands = Brand.objects.all() # Kinpur Artulano
	monthes = Product.objects.filter(manager=manager_id).values('product_name', 'sales', 'date').annotate(month=TruncMonth('date')).annotate(sales_by_month=Sum('sales'))
		
	total_sales=[]
	for item in type:
		name = item.type
		type_sales = 0
		for p in product:
			if name == p.product_name:
				s = p.sales
				type_sales += s
		total_sales.append(type_sales)
	
	return render(request, 'MyPage.html', {'manager':manager_id ,'product' : product, 'managers' : managers, 'type' : type, 'monthes': monthes, 'type_1':total_sales, 'brands':brands})


@csrf_exempt
def productinfo(request, name):
	products = Product.objects.all().filter(product_name=name)
	product_name = products.values('product_name').first()
	manager_name = products.values('manager').first()['manager']
	average_bsr = products.aggregate(Avg('bsr'))
	bsr = str(average_bsr['bsr__avg'])[0:str(average_bsr['bsr__avg']).find('.')]
	average_rating = products.aggregate(Avg('rating'))
	rating = str(average_rating['rating__avg'])[0:3]
	date = products.values('date').annotate(month=TruncMonth('date'))
	asin = products.values('asin').first()['asin'] # dictionary
	link = products.values('link').first()['link'] # dictionary
	link = link[8:]
	event = products.values('event').last()['event']
	sel_acc = products.values('sel_acc').first()['sel_acc']
	link_to_seo = products.values('link_to_seo').first()['link_to_seo']
	last_30 = products.order_by('-id')[0:10:-1]
	date1 = '2020-01-01'
	date2 = datetime.now()
	form = DateForm(request.POST or None)
	if form.is_valid():
		date1 = form.clean_date1()
		date2 = form.clean_date2()
		if date1==None or date2==None:
			date1 = '2020-01-01'
			date2 = datetime.now()
		products = products.filter(date__gte=date1).filter(date__lte=date2)
		last_30 = products
	if products.count() == 0:
		products = Product.objects.all().filter(product_name=name)
	
	sum_sales = products.aggregate(Sum('sales')) 
	sales = sum_sales['sales__sum'] 
	ostatok = TypeOfProduct.objects.filter(type=name).values('ostatki').first()['ostatki']
	
	if products.last() == None:
		data = AddProduct(request.POST or None)
	else:
		data = AddProduct(request.POST or None, instance=products.last())
	
	if request.method == "POST":
		data = AddProduct(request.POST)
		if data.is_valid():
			sales = data.cleaned_data['sales']
			product = data.save(manager_name)
			product.save()
	else:
		data = AddProduct(instance=products.last()) 
		form = DateForm(request.POST or None)
	
	context= {'form' : form, 'date1': date1, 'date2': date2, 'products':products, 'sales':sales, 'bsr':bsr, 'rating':rating, 'name':name, 'data':data, 'asin':asin, 'link':link, 'event':event, 'seller':sel_acc, 'seo':link_to_seo, 'last_30':last_30, 'ostatki':ostatok}
	return render(request, 'Product.html', context)

 

def edit(request, id): #changing data in DB
	try:
		product = Product.objects.get(id=id)
		prod_name = product.product_name
		link = f'/amz/product/{prod_name}'
		form = AddProduct(request.POST or None, instance=product)
		context = {'form':form, 'product':product}
		if request.method == "POST":
			form.save()
			return HttpResponseRedirect(link)
		else:
			return render(request, "edit.html", context)
	except Product.DoesNotExist:
		return HttpResponseNotFound("<h2>Person not found</h2>")


def delete(request, id): # removing data from DB
	try:
		product = Product.objects.get(id=id)
		product.delete()
		prod_name = product.product_name
		link = f'/amz/product/{prod_name}'
		return HttpResponseRedirect(link)
	except Product.DoesNotExist:
		return HttpResponseNotFound("<h2>Person not found</h2>")


# <!-- <form class='form-control' method="POST" action="" >
# {% csrf_token %}
# <div class="row">
# 	   {{ choose_type.type|as_crispy_field }} 
# <div align="center">
# 	<input type="Submit" name="submit" value="Save Product" class="btn btn-danger"/>
# </div>
# </form> -->