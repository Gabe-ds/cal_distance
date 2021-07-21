from django import forms
from .models import *
import os


VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png']

class UploadImageForm(forms.Form):
    image = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
        super(UploadImageForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            
    def clean_image(self):
        image = self.cleaned_data["image"]
        extension = os.path.splitext(image.name)[1]
        
        if not extension.lower() in VALID_EXTENSIONS:
            raise forms.ValidationError(".jpg, .jpeg, .pngのみ対応しています．")
        
        return image