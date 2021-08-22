from django.urls import path
from . import views
from . import forms

urlpatterns = [
	path('MyPage/<str:manager_id>', views.mypage, name = 'manager_page'),
	# path('manager/<int:manager_id>', views.manager_view, name = "manager"),
	path('manager/<str:manager_id>/<str:brandname>', views.brand, name = "brand"),
	path('product/<str:name>', views.productinfo , name = "product"),
	path('regist/', views.registerPage , name = "regist"),
	path('add_new/', views.new_page , name = "adding new"),
	path('motivation/', views.motivation , name = "motivation"),
	path('product/edit/<int:id>/', views.edit),
	path('product/delete/<int:id>/', views.delete),
	path('acos/edit/<int:id>/', views.edit_reklama),
	path('acos/delete/<int:id>/', views.delete_reklama),
	path('akcii/', views.akcii , name = "table"),
	path('dashboard/', views.dash, name = 'dashboard'),
	path('acos/', views.acos, name = 'acos'),
	
]