import datetime
from background_task import background
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Payment, PaymentHistoryForm
from .models import Customer, PaymentHistory
import decimal
from django.db import transaction
from django.contrib import messages


def payment_history(request):
    if request.method == 'POST':
        form = PaymentHistoryForm(request.POST)
        if form.is_valid():
            account_no = form.cleaned_data['account_phone_no']
            pay_history = PaymentHistory.objects.filter(senderPhoneNo=account_no)
            if pay_history:
                return render(request, 'paymentHistory.html', {'form': form, 'paymentHistory': pay_history})
            else:
                return render(request, 'paymentHistory.html', {'form': form, 'noHistory': True})
    else:
        form = PaymentHistoryForm()
    return render(request, 'paymentHistory.html', {'form': form})


def process_payment(request):
    current_time = datetime.datetime.now()
    if request.method == 'POST':

        form = Payment(request.POST)

        if form.is_valid():
            x = form.cleaned_data['payor_no']
            y = form.cleaned_data['payee_no']
            z = decimal.Decimal(form.cleaned_data['amount'])
            payment_date_time = form.cleaned_data['split_date_time_field']
            if payment_date_time:
                sec = (payment_date_time.timestamp() - current_time.timestamp())
                if not Customer.objects.filter(phoneNo=x).exists() or not Customer.objects.filter(phoneNo=y).exists():

                    messages.warning(request, 'Invalid Information, Transaction Failed...!')
                    return HttpResponseRedirect('/')
                else:
                    messages.success(request, f'Congratulations, Your Payment Have Been Scheduled On : {payment_date_time}')
                    payor = Customer.objects.select_for_update().get(phoneNo=x)
                    if payor.balance >= z:
                        notify_user(payor_no=x, payee_no=y, amount=str(z), schedule=round(sec))
                        return HttpResponseRedirect('/')
                    else:
                        messages.success(request, 'Insufficient Balance, Transaction Failed...!')

                        return HttpResponseRedirect('/')

            else:

                if Customer.objects.filter(phoneNo=x).exists() and Customer.objects.filter(phoneNo=y).exists():
                    payor = Customer.objects.select_for_update().get(phoneNo=x)
                    payee = Customer.objects.select_for_update().get(phoneNo=y)

                    if payor.balance >= z:

                        with transaction.atomic():
                            payor.balance -= z
                            payor.save()

                            payee.balance += z
                            payee.save()

                            save_history = PaymentHistory()
                            save_history.senderPhoneNo = x
                            save_history.receiverPhoneNo = y
                            save_history.amount = z
                            save_history.save()

                            messages.success(request, 'Congratulations, Transaction Successful...!')

                            return HttpResponseRedirect('/')
                    else:

                        messages.success(request, 'Insufficient Balance, Transaction Failed...!')

                        return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Invalid Information, Transaction Failed...!')
                    return HttpResponseRedirect('/')
        else:
            print("Invalid")

    else:
        form = Payment()

    return render(request, 'index.html', {'form': form})


@background()
def notify_user(payor_no, payee_no, amount):
    payor = Customer.objects.select_for_update().get(phoneNo=payor_no)
    payee = Customer.objects.select_for_update().get(phoneNo=payee_no)
    amount = int(amount)

    with transaction.atomic():
        payor.balance -= amount
        payor.save()
        payee.balance += amount
        payee.save()
        save_history = PaymentHistory()
        save_history.senderPhoneNo = payor_no
        save_history.receiverPhoneNo = payee_no
        save_history.amount = amount
        save_history.save()
