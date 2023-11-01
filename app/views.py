from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app.paypal import invoice
from app.models import Paypal, Transaction
import json
from datetime import datetime

# 
@login_required
def send_invoice(request):
    context = {}
    context['url'] = False

    if request.method == "POST":
        email = request.POST.get("email")
        paypal_id = request.POST.get("paypal")
        items = json.loads(request.POST.get("items"))
        paypal = Paypal.objects.get(id=paypal_id)   

        context['url'] = invoice(
            client_id = paypal.cid,
            client_secret = paypal.secret,
            merchant_email = paypal.email,
            customer_email = email,
            items = items,
            mode = paypal.mode
        )

        if(context['url'] is not None):
            Transaction.objects.create(
                user = request.user,
                paypal = paypal,
                items = items,
                timestamp = datetime.now(),
                url = context['url']
            )

        return JsonResponse(context, safe=False)

    context['paypals'] = Paypal.objects.all()
    return render(request, 'app/table.html', context)

# 
def signin(request):

    if request.user.is_authenticated:
        return redirect('send_invoice')

    if request.method == "POST":
        signin_form = AuthenticationForm(request, data=request.POST)
        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)
            return redirect('send_invoice')
    else:
        signin_form = AuthenticationForm()
            
    context = {
        "form": signin_form
    }
    return render(request, 'app/signin.html', context)

# 
@login_required
def signout(request):
    logout(request)
    return redirect('signin')
