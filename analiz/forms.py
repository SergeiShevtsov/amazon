from .models import Product, TypeOfProduct, Message, ACOS
from django import forms
import datetime
from django.forms import ModelForm
from django.utils import timezone


class ACOSForm(ModelForm):
	class Meta:
		model = ACOS
		exclude = ()


class MessageForm(ModelForm):
	text = forms.CharField(
	)
	class Meta:
		model = Message
		exclude = () 


class DateForm(forms.Form):
	start_date = forms.DateField(
		widget=forms.DateInput(attrs={'type': 'date'}),
		required=False
	)
	end_date = forms.DateField(
		widget=forms.DateInput(attrs={'type': 'date'}),
		required=False
	)
	def clean_date1(self):
		data1 = self.cleaned_data['start_date']
		# Помните, что всегда надо возвращать "очищенные" данные.
		return data1
	def clean_date2(self):
		data2 = self.cleaned_data['end_date']
		# Помните, что всегда надо возвращать "очищенные" данные.
		return data2


class ChooseType(ModelForm):
	class Meta:
		model = Product
		fields = ('type',)
	def clean_type(self):
		type_one = self.cleaned_data['type']
		# Помните, что всегда надо возвращать "очищенные" данные.
		return type_one


class AddProduct(ModelForm):
	class Meta:
		model = Product
		exclude = ('link', 'asin','positions_by_keys', 'link_to_seo', 'sel_acc', 'fba_inventory')
		# fields = '__all__'
		# exclude = ()
	positions_by_keys = forms.CharField(max_length=40, required=False)
	changes = forms.CharField(max_length=20, required=False)
	offers = forms.CharField(max_length=20, required=False)
	event = forms.CharField(max_length=1000, required=False)

class AddNewProduct(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
		# exclude = ()
		# widgets = {
		# 	'<название поля>' : forms.TextInput(attrs={'class':'form-input'}),
		# }
	positions_by_keys = forms.CharField(max_length=40, required=False)
	changes = forms.CharField(max_length=20, required=False)
	offers = forms.CharField(max_length=20, required=False)
	event = forms.CharField(max_length=20, required=False)

class AddTypeOfProduct(ModelForm):
	
	class Meta:
		model = TypeOfProduct
		fields = '__all__'
	status_min = forms.IntegerField(required=False)
	status_need = forms.IntegerField(required=False)




	
	

	
	