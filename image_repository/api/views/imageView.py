from django.shortcuts import get_object_or_404, redirect
from ..serializers import CreateImageSerializer, ImageSerializer
from ..models import Account, Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status


class ImageAllImagesView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImagePublicImagesView(generics.ListAPIView):
    queryset = Image.objects.filter(private=False)
    serializer_class = ImageSerializer

class PrivateImagesView(generics.ListAPIView):
    queryset = Image.objects.filter(private=True)
    serializer_class = ImageSerializer

class UserImagesView(generics.ListAPIView):
    serializer_class = ImageSerializer
    def get_queryset(self):
       user_pk = self.kwargs['user_pk']
       user = Account.objects.get(pk=user_pk)
       if Image.objects.filter(user=user).exists():
           return Image.objects.filter(user=user)
       else:
           return Response({'Invalid Request': 'User has no images'}, status=status.HTTP_400_BAD_REQUEST)

class ImageAddView(APIView):
    serializer_class = CreateImageSerializer

    def post(self, request, format=None):
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            private = serializer.data.get('private')
            image = request.FILES['image']
            user = Account.objects.filter(email=user.email).first()
            new_image = Image(private=private, image=image, user=user)
            new_image.save()
            return Response(ImageSerializer(new_image).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    

class ImageUpdateView(APIView):
    serializer_class = CreateImageSerializer

    def post(self, request, pk, format=None):
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        imageToUpdate = get_object_or_404(Image, pk=pk)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            imageToUpdate.private= serializer.data.get('private')
            if request.FILES['image']:
                 imageToUpdate.image = request.FILES['image']
            
            imageToUpdate.save()
            return Response(ImageSerializer(imageToUpdate).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
