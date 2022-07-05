from django import forms


class Payment(forms.Form):
    payor_no = forms.CharField(max_length=30, error_messages={'required': "This field is required."})
    payee_no = forms.CharField(max_length=30, error_messages={'required': "This field is required."})
    amount = forms.CharField(max_length=30, error_messages={'required': "This field is required."})
    # day = forms.DateField(initial=datetime.date.today)
    # time = forms.TimeField()
    split_date_time_field = forms.SplitDateTimeField(
        label_suffix=" : "
        ,
        label='Payment Date and Time(Optional) Format: date-%Y-%m-%d  time:%H:%M:%S', required=False,
        disabled=False, input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S"],
        widget=forms.SplitDateTimeWidget(attrs={'class': 'form-control',
                                                'placeholder': 'Date and Time'}),

    )


class PaymentHistory(forms.Form):
    account_phone_no = forms.CharField(max_length=11, error_messages={'required': "This field is required."})
