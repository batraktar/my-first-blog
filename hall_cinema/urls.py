from django.contrib import admin
from django.urls import path, include
from app_cinema.views import MovieListView, SignUp, LogIn, LogOut, HallCreateView, MovieSessionCreateView, \
    MovieSessionEditView, HallEditView, MovieSessionView, TicketPurchaseView, TicketListView, FilmCreateView

urlpatterns = [
    path('', MovieListView.as_view(), name='base'),
    path('admin/', admin.site.urls),
    path('api/', include('app_cinema.api.urls')),
    path('signup/', SignUp.as_view(), name='sing_up'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('create_hall/', HallCreateView.as_view(), name='create_hall'),
    path('create_film/', FilmCreateView.as_view(), name='create_film'),
    path('create_movie_session', MovieSessionCreateView.as_view(), name='create_movie_session'),
    path('movie_session/<slug:slug>', MovieSessionView.as_view(), name='movie_session'),
    path('edit_movie_session/<slug:slug>', MovieSessionEditView.as_view(), name='edit_session'),
    path('edit_hall/<slug:slug>', HallEditView.as_view(), name='edit_hall'),
    path('ticket_purchase/<int:pk>', TicketPurchaseView.as_view(), name="ticket_purchase"),
    path('ticket_list', TicketListView.as_view(), name='ticket_list'),

]
