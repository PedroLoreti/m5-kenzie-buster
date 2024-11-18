from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birthdate = serializers.DateField(required=False)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    password = serializers.CharField(write_only=True)

    class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    def create(self, validated_data):
        errors = {}

        if User.objects.filter(username__iexact=validated_data['username']).exists():
            errors['username'] = ['username already taken.']

        if User.objects.filter(email__iexact=validated_data['email']).exists():
            errors['email'] = ['email already registered.']

        if errors:
            raise serializers.ValidationError(errors)

        if validated_data.get('is_employee'):
            validated_data['is_superuser'] = True

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = make_password(password)

        instance.save()
        return instance