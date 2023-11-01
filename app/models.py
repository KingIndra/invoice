from django.db import models
from django.contrib.auth.models import User


class Paypal(models.Model):
    CHOICES = (
        ("sandbox", "sandbox"),
        ("live", "live"),
    )
    cid = models.CharField(max_length=500)
    secret = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    mode = models.CharField(max_length=10, choices=CHOICES)

    def __str__(self):
        return self.email
    

class Transaction(models.Model):

    paypal = models.ForeignKey(Paypal, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    items = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} | {self.timestamp.now()}"
