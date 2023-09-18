from django.contrib.auth.models import User
from rest_framework import serializers
from app_cinema.models import MovieSession, Hall, Film


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class FilmSerializers(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class HallSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class MovieSessionSerializers(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = '__all__'
