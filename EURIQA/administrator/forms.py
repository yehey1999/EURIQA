from django import forms
from .models import *
from administrator.models import *
from enrollee.models import *

class RegistrationForm(forms.ModelForm):

	class Meta:
		model = enrollee
		fields = ('user', 'address', 'level')