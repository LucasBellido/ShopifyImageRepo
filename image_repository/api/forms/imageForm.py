from django import forms

from ..models import Image

class CreateImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['private', 'image'] 

class UpdateImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['private', 'image']

    def save(self, commit=True):
        obj = self.instance
        obj.private = self.cleaned_data['private']

        if self.cleaned_data['image']:
            obj.image = self.cleaned_data['image']

        if commit:
            obj.save()
        return obj

  