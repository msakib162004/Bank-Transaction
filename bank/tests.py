from django.test import TestCase
from .models import Customer, PaymentHistory

# Create your tests here.


class CustomerTest(TestCase):
    def setUp(self):
        Customer.objects.create(name='Akib', balance=10, phoneNo='01920044879')
        Customer.objects.create(name='Rafid', balance=20, phoneNo='01813156789')

    def test_customer_exist_test(self):
        obj1 = Customer.objects.get(phoneNo='01920044879')
        obj2 = Customer.objects.get(phoneNo='01813156789')
        self.assertEqual(obj1.phoneNo, '01920044879')
        self.assertEqual(obj2.phoneNo, '01813156789')
        self.assertEqual(obj1.balance, 10)
        self.assertEqual(obj2.balance, 20)
