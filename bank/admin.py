from django.contrib import admin

from .models import customer, paymentHistory


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phoneNo', 'balance')


admin.site.register(customer, CustomerAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('senderPhoneNo', 'receiverPhoneNo', 'amount')


admin.site.register(paymentHistory, CustomerAdmin)
