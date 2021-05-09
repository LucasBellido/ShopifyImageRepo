import requests
import factory
from factory.django import DjangoModelFactory
from ..models import Account, Image

def linkFetch():
        url = "https://api.unsplash.com/photos/random/?client_id=xM_nwCT7-8fY9H1z2gjxKj3AJNB-zkp2eGCsxMdQAJ8"
        response = requests.get(url)
        data = response.json()["links"]["download_location"]
        return data


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image 

    id = factory.Sequence(lambda n: n)
    imageURL = linkFetch()
    user = Account.objects.get(pk=1)


t = ImageFactory()
t.id
t.imageURL  # Room marriage study
t.user  # <User: Michelle>

    
