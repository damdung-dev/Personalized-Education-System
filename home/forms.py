# forms.py
from django import forms
from .models import RecommendDocument

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = RecommendDocument
        fields = ['title', 'cover', 'price', 'file']


