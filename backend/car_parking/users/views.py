from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import models, serializers


class RegisterUserAPIView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.User.objects.all()
    serializer_class = serializers.RetrieveAndUpdateUserSerializer


class UserLogIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'contact_number': user.contact_number,
            'is_admin': user.is_superuser
        })


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            request_data = request.data
            user_id = request_data.get('id', None)
            if not user_id:
                return Response({'id': "User Id is required"})
            models.User.objects.get(id=user_id)

        except Exception as err:
            return Response("User Doesn't exist by provided user id")

        else:
            request.user.auth_token.delete()
            return Response("You have been logout successfully!")
