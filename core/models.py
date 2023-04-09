from django.db import models
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image', default='default-avatar-photo')
    location = CountryField(blank=True, null=True)

    def __str__(self):
        return self.user.username