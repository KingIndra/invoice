from django.contrib import admin
from app.models import Paypal, Transaction


admin.site.register(Paypal)
admin.site.register(Transaction)
