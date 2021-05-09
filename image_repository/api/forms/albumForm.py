from django import forms

from ..models import Account, Album

class CreateAlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['name', 'description', 'private', 'users', 'images'] 


class UpdateAlbumInfoForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['name', 'description', 'private'] 

    def save(self, commit=True):
        obj = self.instance
        obj.name = self.cleaned_data['name']
        obj.description = self.cleaned_data['description']
        obj.private = self.cleaned_data['private']

        if commit:
            obj.save()
        return obj

class AddAlbumUsersForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['users'] 

    #users = forms.ModelMultipleChoiceField(queryset=Account.objects.all())

    def save(self, commit=True):
        obj = self.instance
    
        if self.cleaned_data['users']:
            newMembers = self.cleaned_data['users']
            obj.users.add(newMembers)

        if commit:
            obj.save()
        return obj

class AddImageToAlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['images'] 

    def save(self, commit=True):
        obj = self.instance

        if self.cleaned_data['images']:
            newImages = self.cleaned_data['images']
            obj.images.add(newImages)

        if commit:
            obj.save()
        return obj