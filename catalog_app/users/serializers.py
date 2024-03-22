from rest_framework.serializers import ModelSerializer

from .models import User


class CreateUserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}
