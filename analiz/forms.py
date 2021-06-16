from .models import Product
from django import forms
import datetime
from django.forms import ModelForm
from django.utils import timezone




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




class AddProduct(ModelForm):
	class Meta:
		model = Product
		exclude = ('link', 'asin','positions_by_keys')
		# fields = '__all__'
		# exclude = ()
	changes = forms.CharField(max_length=20, required=False)
	offers = forms.CharField(max_length=20, required=False)
	event = forms.CharField(max_length=20, required=False)




	
	

	
	