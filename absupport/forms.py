from django import forms

from product.models import ProductImage

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product_photo']
