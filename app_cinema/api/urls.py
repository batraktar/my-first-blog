from django.urls import path
from app_cinema.api.views import MovieCreateSet, UserRegistrationView, HallCreateView, FilmCreateView

urlpatterns = [
    path('create/movies', MovieCreateSet.as_view(), name='create_session'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('create/hall', HallCreateView.as_view(), name='create__hall'),
    path('create/film', FilmCreateView.as_view(), name='create_film'),

]
