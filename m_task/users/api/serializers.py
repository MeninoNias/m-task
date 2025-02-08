from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from m_task.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        password_confirm = attrs.pop('password_confirm', None)
        password = attrs.get('password')

        if password != password_confirm:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({
                "password": list(e.messages)
            })

        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": "User with this email already exists."
            })

        return attrs

    def create(self, validated_data):
        username = validated_data.get('email')
        password = validated_data.pop('password')

        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                **validated_data,
            )
            user.set_password(password)
            user.save()

        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access = refresh.access_token

        instance.token_jti = access[api_settings.JTI_CLAIM]

        # Retorna os dados básicos do usuário junto com os tokens
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(instance.id),
                'email': instance.email,
                'name': instance.name,
            }
        }
