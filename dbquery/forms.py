from django import forms
from dbquery.models import TarBase
from django.forms import ModelForm

# main user search form
class SearchMainForm(forms.ModelForm):
	class Meta: #define the form
		model = TarBase
		fields = ['miRNA_name']
