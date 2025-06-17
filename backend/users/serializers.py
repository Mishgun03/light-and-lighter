from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # simple-jwt по умолчанию использует username_field = 'username'
    # мы его переопределяем на 'email'
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Вы можете добавить дополнительные данные в токен, если нужно
        # token['username'] = user.username
        # token['email'] = user.email

        return token

    # Переопределяем поле для входа
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = self.fields['password']
        del self.fields['username'] # Удаляем старое поле 'username'

    def validate(self, attrs):
        # Вход по email вместо username
        # Мы ищем пользователя по email и передаем его в родительский validate
        attrs['username'] = User.objects.get(email=attrs[self.username_field]).username
        return super().validate(attrs)
