from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=4)
    password = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ('Username is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
