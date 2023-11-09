from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,verbose_name='user' ,on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    birth_date = models.DateField(null=True, blank=False)

    def __str__(self):
        return self.user.username