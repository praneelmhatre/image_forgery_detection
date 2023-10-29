# forms.py 
from django import forms 
from .models import Images

class ImagesForm(forms.ModelForm): 
    class Meta: 
        model = Images 
        fields = ['uploaded_image','ela_image'] 





