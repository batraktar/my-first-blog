from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import MovieSession


@receiver(pre_save, sender=MovieSession)
def generate_movie_session_slug(sender, instance, **kwargs):
    if not instance.slug:
        film_name = instance.name.name
        hall_name = instance.hall.name
        session_time = instance.start_time.strftime('%H%M')
        session_date = instance.cob_show_time.strftime('%Y%m%d')
        slug = slugify(f"{hall_name}-{film_name}-{session_date}-{session_time}")

        instance.slug = slug
