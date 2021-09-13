from django.urls import path
from . import views
from . import forms
from django.conf.urls import url
from django.views.generic import RedirectView


urlpatterns = [
	# в ссылке и категория и бренд
	path('MyPage/<str:manager_id>', views.mypage, name = 'manager_page'),
	path('manager/<str:manager_id>/<str:brandname>', views.brand, name = "manager&brand"),
	path('manager/<str:manager_id>/<str:cat>', views.brand, name = "manager&brand"),
	path('manager/<str:manager_id>/<str:cat>/<str:brandname>', views.brand, name = "manager&brand"),
	path('product/<str:name>', views.productinfo , name = "product"),
	path('regist/', views.registerPage , name = "regist"),
	path('add_new/', views.new_page , name = "adding new"),
	path('managers_users/', views.managers_users , name = "managers&users"),
	path('motivation/', views.motivation , name = "motivation"),
	path('product/edit/<int:id>/', views.edit),
	path('product/edit_first/<int:id>/', views.edit_first),
	path('motivation/edit_motivation/<int:id>/', views.edit_motivation),
	path('product/delete/<int:id>/', views.delete),
	path('product/edit_type/<int:id>/', views.edit_type),
	path('acos/edit/<int:id>/', views.edit_reklama),
	path('acos/delete/<int:id>/', views.delete_reklama),
	path('akcii/', views.akcii , name = "table"),
	path('dashboard/', views.dash, name = 'dashboard'),
	path('acos/', views.acos, name = 'acos'),
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
]