from rest_framework import serializers as serializers
from account.models import *

from django.contrib.auth import get_user_model

User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("__all__")


class GeneralSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSetting
        fields = ("__all__")


class EmailSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSetting
        fields = ("__all__")


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ("__all__")


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("__all__")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("__all__")


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ("__all__")


class ServerConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerConfig
        fields = ("__all__")


class InferenceAPISerializer(serializers.Serializer):
    operation = serializers.CharField(max_length=10)
