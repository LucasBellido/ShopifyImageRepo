from .models import Album, Image, Account
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'description', 'created_at', 'private', 'users', 'images']

class CreateAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['name', 'description', 'private', 'images'] 

class AlbumAddUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['users'] 
    
class ImageSerializer((serializers.ModelSerializer)):
    class Meta:
        model = Image
        fields = ['id', 'added_at', 'private', 'image', 'imageURL','favorites', 'views', 'user'] 

class CreateImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['private', 'image'] 

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'date_joined']

class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[UniqueValidator(queryset=Account.objects.all())])

    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
    
    def create(self, validated_data):
        account = Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        account.save()
        return account

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        account = authenticate(**data)
        if account and account.is_active:
            return account
        raise serializers.ValidationError("Incorrect Credentials")

