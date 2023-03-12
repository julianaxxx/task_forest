from django import forms
from .models import Pet

class RenamePetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
from django import forms
from .models import Item

class BuyItemForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
