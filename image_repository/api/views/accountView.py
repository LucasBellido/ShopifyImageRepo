from ..models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from ..serializers import LoginSerializer, RegistrationSerializer, AccountSerializer
from rest_framework.authtoken.models import Token

class RegistrationView(APIView):
	serializer_class = RegistrationSerializer

	def post(self, request, format=None):
		serializer = self.serializer_class(data=request.data)
	
		serializer.is_valid(raise_exception=True)
		account = serializer.save()
		token = Token.objects.create(user=account)
		return Response({
			"account": AccountSerializer(account, context=self.serializer_class.context).data,
			"token": token.key
		}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
	serializer_class = LoginSerializer

	def post(self, request, format=None):
		serializer = self.serializer_class(data=request.data)
	
		serializer.is_valid(raise_exception=True)
		account = serializer.validated_data
		try:
			token = Token.objects.get(user_id=account.id)
		except Token.DoesNotExist:
			token = Token.objects.create(user=account)

		return Response({
			"account": AccountSerializer(account, context=self.serializer_class.context).data,
			"token": token.key
		}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
	permission_classes = [
		permissions.IsAuthenticated,
	]

	serializer_class = AccountSerializer

	def get_object(self):
		return self.request.user