from django import forms

from .models import ArtistDesign

class ArtistForm(forms.ModelForm):
    class Meta:
        model = ArtistDesign
        fields = [
            'title',
            'comment',
            'design',
            'tags'
        ]

class ArtistDesignEditForm(forms.ModelForm):
    class Meta:
        model = ArtistDesign
        fields = ['design'
        ]