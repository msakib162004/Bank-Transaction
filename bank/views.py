
import time
#from datetime import datetime
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Payment
from .models import customer
from django.db.models import F
import decimal
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def process_payment(request):
    currentTime = datetime.datetime.now()
    global payor, payee
    if request.method == 'POST':

        form = Payment(request.POST)

        if form.is_valid():
            x = form.cleaned_data['payor']
            y = form.cleaned_data['payee']
            z = decimal.Decimal(form.cleaned_data['amount'])
            PaymentDateTime = form.cleaned_data['split_date_time_field']
            if PaymentDateTime:

                #PaymentDateTime = datetime.strptime(PaymentDateTime, "%Y-%m-%d %H:%M:%S")
                sec = (PaymentDateTime.timestamp() - currentTime.timestamp())
                
                time.sleep(sec)
                if customer.objects.filter(name=x).exists() and customer.objects.filter(name=y).exists():
                    payor = customer.objects.select_for_update().get(name=x)
                    payee = customer.objects.select_for_update().get(name=y)

                    with transaction.atomic():
                        payor.balance -= z
                        payor.save()

                        payee.balance += z
                        payee.save()

                        # customer.objects.filter(name=x).update(balance=F('balance') - z)
                        # customer.objects.filter(name=y).update(balance=F('balance') + z)
                        messages.success(request, 'Congratulations, Transaction Successful...!')  # ignored

                        return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Invalid Information, Transaction Failed...!')  # recorded
                    return HttpResponseRedirect('/')
            else:

                if customer.objects.filter(name=x).exists() and customer.objects.filter(name=y).exists():
                    payor = customer.objects.select_for_update().get(name=x)
                    payee = customer.objects.select_for_update().get(name=y)

                    with transaction.atomic():
                        payor.balance -= z
                        payor.save()

                        payee.balance += z
                        payee.save()

                        # customer.objects.filter(name=x).update(balance=F('balance') - z)
                        # customer.objects.filter(name=y).update(balance=F('balance') + z)
                        messages.success(request, 'Congratulations, Transaction Successful...!')  # ignored

                        return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Invalid Information, Transaction Failed...!')  # recorded
                    return HttpResponseRedirect('/')
        else:
            print("Invalid")

        # customerData = customer.objects.all()

    else:
        form = Payment()

    return render(request, 'index.html', {'form': form})
