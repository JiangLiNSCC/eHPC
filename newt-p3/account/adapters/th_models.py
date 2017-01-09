from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# # Create your models here.
# class Cred(models.Model):
#     class Meta:
#         app_label = 'authnz'
#     cert = models.TextField()
#     key = models.TextField()
#     calist = models.TextField()
#     user = models.ForeignKey(User)

class Account(models.Model):
    account = models.CharField(max_length=100)
    def __str__(self):
        return self.account

class AccountActive(models.Model):
    user = models.OneToOneField(
        User , on_delete=models.CASCADE,
        related_name="account_active",
    )
    account = models.ForeignKey(
        Account ,
        on_delete=models.CASCADE ,
        related_name="account_active",
                                       )
    def __str__(self):
        return self.user.__str__() + self.account.__str__()



class UserAccount(models.Model):
    user = models.ForeignKey(
        User , on_delete=models.CASCADE
    )
    account = models.ForeignKey(Account , on_delete=models.CASCADE)