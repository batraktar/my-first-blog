from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from app_cinema.forms import UserCreateForm, HallForm, MovieSessionForm, UserLoginForm, TicketPurchaseForm, FilmForm
from app_cinema.models import MovieSession, Hall, Ticket


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SignUp(CreateView):
    template_name = 'sign-up.html'
    form_class = UserCreateForm
    success_url = '/'


class LogIn(LoginView):
    template_name = 'log-in.html'
    form_class = UserLoginForm
    next_page = '/'


class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        total_spent = Ticket.objects.filter(user=user).aggregate(total=Sum('total_price'))['total']
        context['total_spent'] = total_spent
        return context


class LogOut(LoginRequiredMixin, LogoutView):
    next_page = '/'


class HallCreateView(AdminPassedMixin, CreateView):
    form_class = HallForm
    template_name = 'create_hall.html'
    success_url = '/'


class HallEditView(AdminPassedMixin, UpdateView):
    model = Hall
    form_class = HallForm
    template_name = 'edit_hall.html'
    success_url = '/'


class FilmCreateView(AdminPassedMixin, CreateView):
    form_class = FilmForm
    template_name = 'create_film.html'
    success_url = '/'


class MovieSessionCreateView(AdminPassedMixin, CreateView):
    form_class = MovieSessionForm
    template_name = 'create_moviesession.html'
    success_url = '/'

    def form_valid(self, form):
        hall = form.cleaned_data['hall']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        cob_show_time = form.cleaned_data['cob_show_time']
        ended_show_time = form.cleaned_data['ended_show_time']

        current_date = cob_show_time
        while current_date <= ended_show_time.date():
            if MovieSession.objects.filter(hall=hall, cob_show_time=current_date, start_time__lt=end_time,
                                           end_time__gt=start_time).exists():
                messages.error(self.request, 'Помилка: Сеанси перекриваються!')
                return self.form_invalid(form)

            movie_session = form.save(commit=False)
            movie_session.cob_show_time = current_date
            movie_session.ended_show_time = current_date
            movie_session.save()

            current_date += timedelta(days=1)

        return super().form_valid(form)


class MovieSessionView(LoginRequiredMixin, DetailView):
    model = MovieSession
    template_name = 'detailed_session_overview.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TicketPurchaseForm()
        return context


class MovieSessionEditView(AdminPassedMixin, UpdateView):
    model = MovieSession
    form_class = MovieSessionForm
    template_name = 'edit_session.html'
    success_url = '/'
    slug_field = 'slug'

    def form_valid(self, form):
        hall = form.cleaned_data['hall']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']

        if MovieSession.objects.filter(hall=hall, start_time__lt=end_time, end_time__gt=start_time).exists():
            messages.error(self.request, 'Помилка: Сеанси перекриваються!')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        session = self.get_object()
        tickets_sold = Ticket.objects.filter(session=session).exists()
        if tickets_sold:
            messages.warning(request, 'Tickets have been sold for this session. Proceed with caution.')
        return super().get(request, *args, **kwargs)


class MovieListView(ListView):
    model = MovieSession
    template_name = 'base.html'
    slug_field = 'slug'
    paginate_by = 6

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by')

        if sort_by == 'ticket_price':
            self.ordering = ['ticket_price']
        else:
            self.ordering = ['start_time']

        queryset = super().get_queryset()
        return queryset


class TicketPurchaseView(LoginRequiredMixin, CreateView):
    def post(self, request, pk):
        quantity = int(request.POST.get('quantity'))
        user = request.user

        with transaction.atomic():
            session = MovieSession.objects.select_for_update().get(pk=pk)

            if session.available_seats >= quantity:
                ticket_price = session.ticket_price * quantity

                if user.wallet >= ticket_price:
                    ticket = Ticket(session=session, user=user, quantity=quantity, total_price=ticket_price)
                    ticket.save()

                    session.available_seats -= quantity
                    session.save()

                    user.wallet -= ticket_price
                    user.save()

                    return redirect('/')
                else:
                    messages.error(request, "Недостатньо коштів на рахунку.")
            else:
                messages.error(request, "Недостатня кількість вільних місць.")
        return redirect('/')
