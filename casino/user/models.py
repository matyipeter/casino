from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,verbose_name='user' ,on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    birth_date = models.DateField(null=True, blank=False)

    def __str__(self):
        return self.user.username


class WinningHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="user", on_delete=models.CASCADE)
    win = models.FloatField(default=0.00)
    win_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username


class TransactionHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete=models.CASCADE)
    flow = models.FloatField(default=0.00)
    transaction_date = models.DateTimeField()

    def __str__(self):
        return self.user.user.username
    
    def save(self, *args, **kwargs):
         self.user.balance += self.flow
         self.user.save()
         super().save(*args, **kwargs)