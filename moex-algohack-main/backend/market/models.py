from django.db import models


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)

