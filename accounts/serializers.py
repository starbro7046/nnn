from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def validate_password(self, value: str) -> str:
        return make_password(value)