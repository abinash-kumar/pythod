from django import forms

from .models import Customer

class CustomerImageForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'user_photo'
        ]