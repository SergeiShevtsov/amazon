from django.urls import path
from . import views
from . import forms

urlpatterns = [
	path('MyPage/<int:manager_id>', views.mypage, name = 'manager_page'),
	path('manager/<int:manager_id>', views.manager_view, name = "manager"),
	path('manager/<int:manager_id>/<str:brandname>', views.brand, name = "brand"),
	path('product/<str:name>', views.productinfo , name = "product"),
	path('regist', views.registerPage , name = "regist"),
	path('motivation/', views.motivation , name = "motivation"),
]