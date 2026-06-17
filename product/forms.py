from django.forms import FileInput, ModelForm, ImageField, ClearableFileInput
from .models import Product, Image

class MultipleFileInput(FileInput):
    allow_multiple_selected = True

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', "price", "valute", 'status', 'description']

class ImageForm(ModelForm):
    image = ImageField(widget=MultipleFileInput())

    class Meta:
        model = Image
        fields = ['image']
