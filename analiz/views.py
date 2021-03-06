from .models import Product, Manager, Brand, TypeOfProduct, Message, ACOS, Category
from django.shortcuts import render, redirect
from django.db.models import Sum, Avg
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import DateForm, AddProduct, AddNewProduct, AddTypeOfProduct, ChooseType, MessageForm, ACOSForm, Managersform, UsersForm, ChangeLink
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models.functions import ExtractMonth, TruncMonth
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User, Group
import gspread
import pandas as pd
import gspread
import pandas as pd
import re


# обьединять данные по двум товаров с одного склада за один день
def sentry(request, test=1):
    added_products = []
    new_products = []
    gc = gspread.service_account(filename='sentrykit-24ddd78fce35.json')
    sh = gc.open("SentryKit sheets") # выбор электронной таблицы

    sales = sh.worksheet("Sales")
    data_sales = sales.get_all_records()
    dash = sh.worksheet("Dashboard")
    data_dash = dash.get_all_records()

    try:
        counter = 0
        for dict in data_dash:
            if dict['ASIN'] == data_sales[counter]['ASIN']:
                dict['Sales'] = data_sales[counter]['Yesterday\'s Sales (units)']
                dict['Date'] = data_sales[counter]['Yesterday\'s Date on Marketplace']
                counter += 1
            else:
                dict['Sales'] = 'No'
                dict['Date'] = '(untracked)'
    except:
        pass 
    

    for item in data_dash:
		
        if item['Date'] == '(untracked)':
            continue
	
        product = Product.objects.filter(asin = item['ASIN']).last()
        try:
            id = product.id
        except:
            new_products.append(item['Product Short Name'])
            continue

        if str(product.date) == item['Date']:
            product.sales += item['Sales']
            product.save()
            continue
        product.id=None 
        product.date=item["Date"]
        product.sales=item["Sales"]
        try:
            new_price = re.findall(r'\d+', item['Price']) 
            product.price=float('.'.join(new_price))
        except:
            pass
        new_rating = float(re.findall(r'\d+', item['Star Rating'])[0])
		
        product.rating=new_rating
        product.link=item['Amazon URL']
        product.fba_inventory=item['FBA Inventory']
        product.save()
        added_products.append(product)

    context = {'new_products':data_sales, 'products':added_products, 'new_items':new_products}
    return render(request, 'Sentry.html', context)



@cache_page(60*10) # установить время для кеширования main page 
@csrf_exempt
def mypage(request, manager_id, brandname=None):	
	if request.user.id:
		pass
	else:
		return render(request, 'MyPage.html')
	current_user = request.user.id 
	user = User.objects.get(id=current_user)
	
	if user.groups.filter(name='Boss').exists():
		manager_id = Manager.objects.get(id=manager_id)
	else:
		manager_id = Manager.objects.get(id=current_user) 
	
	product = Product.objects.select_related('manager', 'type', 'brand').order_by('manager')
	
	managers = []
	type = []
	brands = Brand.objects.all() # можно попробовать методы сортировки
	# brands = []
	for item in product:
		if item.manager not in managers:
			managers.append(item.manager)

	
	for item in product:
		if item.type not in type and item.manager == manager_id:
			type.append(item.type)
	
	categories = Category.objects.all()
	
	date3 = datetime.now()
	date1 = f'{date3.timetuple()[0]}-{date3.timetuple()[1]-1}-01' 
	date2 = f'{date3.timetuple()[0]}-{date3.timetuple()[1]}-01' 	
	
	form = DateForm(request.POST or None)
	got_items = '0'
	if form.is_valid():
		got_items = '1'
		date1 = form.clean_date1()
		date2 = form.clean_date2()
		if date1==None or date2==None:
			date1 = '2020-01-01'
			date2 = datetime.now()
		product = product.filter(date__gte=date1).filter(date__lte=date2)
	else:
		product = product.filter(date__gte=date1).filter(date__lte=date2)
	
	last_products = product.filter(manager=manager_id).order_by('-date')[0:len(type)]

	if len(type) == 0:
		for item in product:
			if item.type not in type:
				type.append(item.type)
	
	# разобраться с максимом отдельный def вызывающийся когда нужно
	maxim_list = []
	for i in type:
		if i.owner == "max" or i.owner == "Max":
			maxim_list.append(i)
		else:
			pass
	
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
		for p in product.order_by('-date'):
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
		
	context = {'got_items':got_items, 'form':form, 'product' : product, 'managers' : managers, 'type' : type, 'type_1':total_sales,'ave_sales':ave_sales , 'brands':brands, 'manage_id' : manager_id, 'money':got_money, 'maxim':maxim_list, 'max_total_sales':max_total_sales, 'max_ave_sales':max_ave_sales, 'max_got_money':max_got_money, 'last_products':last_products, 'current_user':current_user, 'categories':categories}
	
	
	return render(request, 'MyPage.html', context)


@csrf_exempt
# @cache_page(60*60*4) 
def productinfo(request, name):
	type = TypeOfProduct.objects.filter(type=name).first()
	products = Product.objects.all().filter(product_name=name)
	first_product = products.first()
	product_name = products.values('product_name').first()
	manager_name = products.values('manager').first()['manager']
	
	date = products.values('date').annotate(month=TruncMonth('date'))
	asin = products.values('asin').first()['asin'] # dictionary
	link = products.values('link').first()['link'] # dictionary
	link = link[8:]
	
	type_id = TypeOfProduct.objects.filter(type=name).values('id').first()['id'] # 35
	messages = Message.objects.filter(product_type=type_id).order_by('-id')
	coun = 0
	average_sales = 0
	for p in products:
		if type == p.product_name:
			s = p.sales
			average_sales += s
			coun += 1
	if coun == 0:
		coun = 1
	average_sales = average_sales / coun
	average_sales = round(average_sales,0)

	
	event = products.values('event').last()['event']
	sel_acc = products.values('sel_acc').first()['sel_acc']
	link_to_seo = products.values('link_to_seo').first()['link_to_seo']
	last_30 = products.order_by('-date')[0:10:-1]
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
		messages = Message.objects.filter(product_type=type_id).filter(date__gte=date1).filter(date__lte=date2).order_by('-id')
	if products.count() == 0:
		products = Product.objects.all().filter(product_name=name)
	
	average_bsr = products.aggregate(Avg('bsr'))
	bsr = str(average_bsr['bsr__avg'])[0:str(average_bsr['bsr__avg']).find('.')]
	average_rating = products.aggregate(Avg('rating'))
	rating = str(average_rating['rating__avg'])[0:3]
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
		
	
	last_message = Message.objects.filter(product_type=type_id).last()
	
	chat_form = MessageForm(request.POST or None)
	if request.method == 'POST' and chat_form.is_valid():
		chat_form.save()
	else:
		chat_form = MessageForm(request.POST or None, instance=last_message)
	
	
	context= {'form' : form, 'date1': date1, 'date2': date2, 'products':products, 'sales':sales, 'bsr':bsr, 'rating':rating, 'name':name, 'data':data, 'asin':asin, 'link':link, 'event':event, 'seller':sel_acc, 'seo':link_to_seo, 'last_30':last_30, 'ostatki':ostatok, 'chat':chat_form, 'messages':messages, 'type_o':type, 'ave_sales':average_sales, 'first_product':first_product}
	return render(request, 'Product.html', context)


def managers_users(request):
	manager = Managersform(request.POST or None)
	user = UsersForm(request.POST or None)
	if request.method == 'POST' and manager.is_valid():
		manager.save()	
	elif request.method == 'POST' and user.is_valid():
		user.save()
	# elif choose_type.is_valid() and request.method == "POST":
	# 	data = choose_type.clean_type()
	# 	prod = Product.objects.filter(type=data).last()
	# 	new_product = AddNewProduct(request.POST or None, instance=prod)
	else:
		manager = Managersform(request.POST or None)
		user = UsersForm(request.POST or None)
	
	context = {'new_manager':manager, 'new_user':user}
	return render(request, 'Managers&Users.html', context)


def acos(request):
	products = ACOS.objects.all()	
	add_acos = ACOSForm(request.POST)
	if request.method == 'POST':
		data = ACOSForm(request.POST)
		if data.is_valid():
			add_acos.save()
	else:
		add_acos = ACOSForm(request.POST or None)
	
	context = {
		'acos':products,
		'form':add_acos,
	}
	
	return render(request, 'ACOS.html', context)

# пытаюсь добавить красивый шаблон с bootstrap
def dash(request):
	return render(request, 'dashboard.html')


def akcii(request):
	type = TypeOfProduct.objects.all().order_by('type')
	max_types = type.filter(owner='Max')
	products = Product.objects.all()
	max_sales = []
	max_money = []
	total_sales = []
	ave_sales = []
	got_money = []
	
	# вывод информации за два последних месяца
	sales_by_month = products.annotate(month=ExtractMonth('date')).values('month').last()['month'] 
	sales_by_premonth = sales_by_month - 1 
	date_1 = f'2021-{sales_by_premonth}-01' # предпоследний месяц
	date_2 = f'2021-{sales_by_month}-01' # последний месяц
	sales_last_month = products.filter(date__gte=date_2).order_by('product_name') # продукты за последний месяц
	sales_1 = []
	sales_2 = []
	sales_last_premonth = products.filter(date__gte=date_1).filter(date__lte=date_2).order_by('product_name') # продукты за предпоследний месяц
	for item in type:
		name = item.type
		sales = 0
		coun = 0
		for p in sales_last_month:
			if name == p.product_name:
				coun += 1
				s = p.sales
				sales += s
		sales_1.append(sales)
	
	for item in type:
		name = item.type
		sales = 0
		for p in sales_last_premonth:
			if name == p.product_name:
				s = p.sales
				sales += s
		sales_2.append(sales)
		
		
	# форма для фильтрации по дате  
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

		if item.owner == 'Max' or item.owner == 'max':
			max_sales.append(type_sales)
			max_money.append(money)
	
	

	context = {'sales':total_sales, 'money':got_money, 'type':type, 'form':form, 'max_sales':max_sales, 'max_money':max_money, 'max_types':max_types, 'sales_1':sales_1, 'sales_2':sales_2, 'sales_last_month':sales_last_month, 'sales_by_premonth':sales_last_premonth}
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
		if (average_sales / int(item.status_min) > 0.9) and (average_sales / int(item.status_need) < 0.9):
			average_sales = f'{average_sales} - 50 BYN'
		elif (average_sales / int(item.status_min) > 0.9) and (average_sales / int(item.status_need) > 0.9):
			average_sales = f'{average_sales} - 100 BYN'
		else:
			average_sales = f'{average_sales}'
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

# сначала бренд - потом категория
def brand(request, manager_id, brandname=None, cat=None):
	brands = Brand.objects.all()
	managers = Manager.objects.all().order_by('username')
	categories = Category.objects.all()
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
	
	return render(request, 'BrandCategory.html', {'form':form, 'product' : product, 'managers' : managers, 'type' : type, 'type_1':total_sales,'ave_sales':ave_sales , 'brands':brands, 'manage_id' : manager_id, 'categories':categories, 'brand_id':brandname, 'cat':cat})


def brand_category(request, manager_id, brandname=None, cat=None):
	brands = Brand.objects.all()
	managers = Manager.objects.all()
	categories = Category.objects.all()
	type = TypeOfProduct.objects.all().filter(brand=brandname, category=cat)
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
	
	return render(request, 'BrandCategory.html', {'form':form, 'product' : product, 'managers' : managers, 'type' : type, 'type_1':total_sales,'ave_sales':ave_sales , 'brands':brands, 'manage_id' : manager_id, 'categories':categories, 'brand_id':brandname, 'cat':cat})



def category(request, manager_id, brandname=None, cat=0):
	brands = Brand.objects.all()
	managers = Manager.objects.all()
	categories = Category.objects.all()

	type = TypeOfProduct.objects.all().filter(category=cat)
	product = Product.objects.all()	

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
	
	return render(request, 'MyPage.html', {'form':form, 'product' : product, 'managers' : managers, 'type' : type, 'type_1':total_sales,'ave_sales':ave_sales , 'brands':brands, 'manage_id' : manager_id, 'categories':categories, 'cat':cat})

 
def edit_first(request, id): # changing data in DB
	try:
		product = Product.objects.get(id=id)
		prod_name = product.product_name
		link = f'/amz/product/{prod_name}'
		form = ChangeLink(request.POST or None, instance=product)
		context = {'form':form, 'product':product}
		if request.method == "POST":
			form.save()
			return HttpResponseRedirect(link)
		else:
			return render(request, "edit.html", context)
	except Product.DoesNotExist:
		return HttpResponseNotFound("<h2>Product not found</h2>")
 

def edit(request, id): # changing data in DB
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
		return HttpResponseNotFound("<h2>Product not found</h2>")


def delete(request, id): # removing data from DB
	try:
		product = Product.objects.get(id=id)
		product.delete()
		prod_name = product.product_name
		link = f'/amz/product/{prod_name}'
		return HttpResponseRedirect(link)
	except Product.DoesNotExist:
		return HttpResponseNotFound("<h2>Person not found</h2>")


def edit_reklama(request, id): #changing data in DB
	try:
		product = ACOS.objects.get(id=id)
		prod_name = product.product_name
		link = f'/amz/acos'
		form = ACOSForm(request.POST or None, instance=product)
		context = {'form':form, 'product':product}
		if request.method == "POST":
			form.save()
			return HttpResponseRedirect(link)
		else:
			return render(request, "edit.html", context)
	except Product.DoesNotExist:
		return HttpResponseNotFound("<h2>Запись не найдена</h2>")


def delete_reklama(request, id): # removing data from DB
	try:
		product = ACOS.objects.get(id=id)
		product.delete()
		prod_name = product.product_name
		link = f'/amz/acos'
		return HttpResponseRedirect(link)
	except Product.DoesNotExist:
		return HttpResponseNotFound("<h2>Запись не найдена</h2>")


def edit_type(request, id): # removing data from DB
	try:
		type = TypeOfProduct.objects.get(id=id)
		name = type.type
		product = Product.objects.filter(product_name=name).last()
		prod_name = product.product_name
		link = f'/amz/product/{prod_name}'
		form = AddTypeOfProduct(request.POST or None, instance=type)
		context = {'form':form, 'type':type}
		if request.method == "POST":
			form.save()
			return HttpResponseRedirect(link)
		else:
			return render(request, "edit.html", context)
	except TypeOfProduct.DoesNotExist:
		return HttpResponseNotFound("<h2>Запись не найдена</h2>")


def edit_motivation(request, id):
	try:
		type = TypeOfProduct.objects.get(id=id)
		# product = Product.objects.get(id=id)
		# prod_name = product.product_name
		link = f'/amz/motivation' 
		form = AddTypeOfProduct(request.POST or None, instance=type)
		context = {'form':form, 'type':type}
		if request.method == "POST":
			form.save()
			return HttpResponseRedirect(link)
		else:
			return render(request, "edit.html", context)
	except TypeOfProduct.DoesNotExist:
		return HttpResponseNotFound("<h2>Запись не найдена</h2>")
