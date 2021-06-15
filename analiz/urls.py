from django.urls import path
from . import views

urlpatterns = [
	path('MyPage/<int:manager_id>', views.mypage, name = 'manager_page'),
	path('manager/<int:manager_id>', views.manager_view, name = "manager"),
	path('manager/<int:manager_id>/<str:brandname>', views.brand, name = "brand"),
	path('product/<str:name>', views.productinfo , name = "product"),
	path('regist', views.registerPage , name = "regist"),
	path('manager/<int:manager_id>/<int:year>', views.filter_by_date, name = "filter_by_date"),
]