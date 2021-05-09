from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Album, Image
from ..serializers import AlbumAddUsersSerializer, AlbumSerializer, CreateAlbumSerializer
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, status
from ..models import Account

class AllAlbumsView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumAddView(APIView):
    serializer_class = CreateAlbumSerializer

    def post(self, request, format=None):
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            print('i got here')
            name = serializer.data.get('name')
            description = serializer.data.get('description')
            private = serializer.data.get('private')

            user = Account.objects.filter(email=user.email).first()
        
            imageIDs = serializer.data.get('images')
            images = Image.objects.filter(pk__in=imageIDs)
            
            new_album = Album(name=name,description=description,private=private)
            new_album.save()
            
            new_album.users.add(user)

            for image in images:
                new_album.images.add(image)

            new_album.save()

            return Response(AlbumSerializer(new_album).data, status=status.HTTP_201_CREATED)
        print(serializer.data)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class UserAlbumsView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    def get_queryset(self):
       user_pk = self.kwargs['user_pk']
       user = Account.objects.get(pk=user_pk)
       if Album.objects.filter(users=user).exists():
           return Album.objects.filter(users=user)
       else:
           return Response({'Invalid Request': 'User has no albums'}, status=status.HTTP_400_BAD_REQUEST)

class AlbumUpdateView(APIView):
    serializer_class = CreateAlbumSerializer

    def post(self, request, pk, format=None):
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        albumToUpdate = get_object_or_404(Album, pk=pk)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            albumToUpdate.name = serializer.data.get('name')
            albumToUpdate.description = serializer.data.get('description')
            albumToUpdate.private = serializer.data.get('private')
            if serializer.data.get('images'):
                imageIDs = serializer.data.get('images')
                images = Image.objects.filter(pk__in=imageIDs)
                for image in images:
                    albumToUpdate.images.add(image)
            
            albumToUpdate.save()
            return Response(AlbumSerializer(albumToUpdate).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class AlbumAddUsersView(APIView):
    serializer_class = AlbumAddUsersSerializer

    def post(self, request, pk, format=None):
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        albumToUpdate = get_object_or_404(Album, pk=pk)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.data.get('users'):
                newUsers = serializer.data.get('users')
                users = Account.objects.filter(pk__in=newUsers)
                for user in users:
                    albumToUpdate.users.add(user)
            
            albumToUpdate.save()
            return Response(AlbumSerializer(albumToUpdate).data, status=status.HTTP_200_OK)
            
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
