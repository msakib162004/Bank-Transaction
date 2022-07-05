from django.contrib import admin

from .models import Customer, PaymentHistory


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phoneNo', 'balance')


admin.site.register(Customer, CustomerAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('senderPhoneNo', 'receiverPhoneNo', 'amount', 'dateTime')


admin.site.register(PaymentHistory, CustomerAdmin)
