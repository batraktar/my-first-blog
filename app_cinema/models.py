from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class UserProfile(AbstractUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=10000)

    def __str__(self):
        return f'Name: {self.username}'


class Hall(models.Model):
    name = models.CharField(max_length=100)
    size = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=1234)

    def __str__(self):
        return self.name


class MovieSession(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    name = models.ForeignKey(Film, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    cob_show_time = models.DateField()
    ended_show_time = models.DateField()
    available_seats = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.available_seats = self.hall.size
        super().save(*args, **kwargs)

    def clean(self):
        if self.ended_show_time < self.cob_show_time:
            raise ValidationError("End date must be after start date.")


class Ticket(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
