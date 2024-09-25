from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not ' \
                                        'match valid image extensions.')
        return url

    def save(self, force_insert=False,
                   force_update=False,
                   commit=True): 
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)#esta-es-una-imagen (slugify)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}' #crea el nombre de la imagen insertada
        # descarga la imagen de internet
        response = requests.get(image_url, verify=False) #verify=false para el error con el SSL
        image.image.save(image_name,
                         ContentFile(response.content), #se guarda la imagen con el contenido que haya llegado
                         save=False)
        if commit:
            image.save()
        return image 