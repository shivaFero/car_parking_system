from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(), message="This email already exits",
    )])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)

    token = serializers.SerializerMethodField()
    is_admin = serializers.CharField(source='is_superuser', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'contact_number', 'password', 'confirm_password',
                  'email', 'token', 'is_admin')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_null': False, 'allow_blank': False},
            'last_name': {'required': True, 'allow_null': False, 'allow_blank': False},
            'contact_number': {'required': True, 'allow_null': False, 'allow_blank': False,
                               'min_length': 10, 'max_length': 12}
        }

    def get_token(self, instance):
        if self.instance:
            token, created = Token.objects.get_or_create(user=instance)
            return token.key
        return None

    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password', None)
        password = attrs.get('password', None)
        if not password == confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Password not matched'})
        return attrs

    def create(self, validated_data):
        # user = User(**validated_data)
        user = super().create(validated_data=validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user


class RetrieveAndUpdateUserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'contact_number', 'password', 'email', 'confirm_password')

    def update(self, instance, validated_data):
        user = super(RetrieveAndUpdateUserSerializer, self).update(instance, validated_data)
        if validated_data.get('password', None):
            user.set_password(validated_data['password'])
            user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'contact_number', 'email')

