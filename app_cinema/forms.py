from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app_cinema.models import UserProfile, Hall, MovieSession, Ticket, Film


class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = (
            'name',
            'size'
        )


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'


class MovieSessionForm(forms.ModelForm):
    cob_show_time = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'})
    )
    ended_show_time = forms.DateTimeField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'})
    )

    class Meta:
        model = MovieSession
        fields = (
            'name',
            'hall',
            'start_time',
            'end_time',
            'cob_show_time',
            'ended_show_time',
            'ticket_price'
        )


class TicketPurchaseForm(forms.ModelForm):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ticket
        fields = (
            'quantity',
        )
