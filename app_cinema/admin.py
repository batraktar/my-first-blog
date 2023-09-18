from django.contrib import admin

from app_cinema.models import UserProfile, Hall, Ticket, MovieSession, Film

admin.site.register(UserProfile)
admin.site.register(Hall)
admin.site.register(Film)
admin.site.register(Ticket)
admin.site.register(MovieSession)
