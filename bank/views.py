import time
import datetime
import multiprocessing

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Payment, PaymentHistory
from .models import customer, paymentHistory
from django.db.models import F
import decimal
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def payment_history(request):

    if request.method == 'POST':
        form = PaymentHistory(request.POST)
        if form.is_valid():
            account_no = form.cleaned_data['account_phone_no']
            payHistory = paymentHistory.objects.filter(senderPhoneNo=account_no)
            for i in payHistory:
                print(i.senderPhoneNo, i.receiverPhoneNo, i.amount)
            return render(request, 'paymentHistory.html', {'form': form, 'paymentHistory': payHistory})
    else:
        form = PaymentHistory()
    return render(request, 'paymentHistory.html', {'form': form})


def process_payment(request):
    currentTime = datetime.datetime.now()
    global payor, payee
    if request.method == 'POST':

        form = Payment(request.POST)

        if form.is_valid():
            x = form.cleaned_data['payor_no']
            y = form.cleaned_data['payee_no']
            z = decimal.Decimal(form.cleaned_data['amount'])
            PaymentDateTime = form.cleaned_data['split_date_time_field']
            if PaymentDateTime:

                # PaymentDateTime = datetime.strptime(PaymentDateTime, "%Y-%m-%d %H:%M:%S")
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

                        saveHistory = paymentHistory()
                        saveHistory.senderPhoneNo = x
                        saveHistory.receiverPhoneNo = y
                        saveHistory.amount = z
                        saveHistory.save()
                        # customer.objects.filter(name=x).update(balance=F('balance') - z)
                        # customer.objects.filter(name=y).update(balance=F('balance') + z)
                        messages.success(request, 'Congratulations, Transaction Successful...!')  # ignored

                        return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Invalid Information, Transaction Failed...!')  # recorded
                    return HttpResponseRedirect('/')
            else:

                if customer.objects.filter(phoneNo=x).exists() and customer.objects.filter(phoneNo=y).exists():
                    payor = customer.objects.select_for_update().get(phoneNo=x)
                    payee = customer.objects.select_for_update().get(phoneNo=y)

                    with transaction.atomic():
                        payor.balance -= z
                        payor.save()

                        payee.balance += z
                        payee.save()

                        saveHistory = paymentHistory()
                        saveHistory.senderPhoneNo = x
                        saveHistory.receiverPhoneNo = y
                        saveHistory.amount = z
                        saveHistory.save()

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
