from django import forms
from .models import literature

class LiteratureForm(forms.ModelForm):
    class Meta:
        model = literature
        fields = '__all__'
