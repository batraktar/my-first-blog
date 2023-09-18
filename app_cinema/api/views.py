from rest_framework import generics
from app_cinema.api.serializers import MovieSessionSerializers, UserRegistrationSerializer, HallSerializers, \
    FilmSerializers
from app_cinema.models import MovieSession, Hall, Film


class MovieCreateSet(generics.CreateAPIView):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializers


class HallCreateView(generics.CreateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializers


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class FilmCreateView(generics.CreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializers
