import datetime
from background_task import background
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Payment, PaymentHistory
from .models import customer, paymentHistory
import decimal
from django.db import transaction
from django.contrib import messages


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

                sec = (PaymentDateTime.timestamp() - currentTime.timestamp())

                if not customer.objects.filter(phoneNo=x).exists() or not customer.objects.filter(phoneNo=y).exists():

                    messages.warning(request, 'Invalid Information, Transaction Failed...!')  # recorded
                    return HttpResponseRedirect('/')
                else:
                    messages.success(request, f'Congratulations, Your Payment Have Been Scheduled On : {PaymentDateTime}') # ignored

                    notify_user(payor_no=x, payee_no=y, amount=str(z), schedule=round(sec))
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

                        messages.success(request, 'Congratulations, Transaction Successful...!')  # ignored

                        return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Invalid Information, Transaction Failed...!')  # recorded
                    return HttpResponseRedirect('/')
        else:
            print("Invalid")

    else:
        form = Payment()

    return render(request, 'index.html', {'form': form})


@background()
def notify_user(payor_no, payee_no, amount):
    payor = customer.objects.select_for_update().get(phoneNo=payor_no)
    payee = customer.objects.select_for_update().get(phoneNo=payee_no)
    with transaction.atomic():
        payor.balance -= int(amount)
        payor.save()
        payee.balance += int(amount)
        payee.save()
        saveHistory = paymentHistory()
        saveHistory.senderPhoneNo = payor_no
        saveHistory.receiverPhoneNo = payee_no
        saveHistory.amount = int(amount)
        saveHistory.save()
