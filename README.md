# Bank-Transaction

Features:

	1. Instant Payment
	2. Scheduled Payment


Setup:

Create a virtual environment using requirments.txt

Run migration commands : 

	python manage.py makemigrations bank
	Python manage.py migrate


Homepage URL : http://127.0.0.1:8000/


Run instructions:

	Open two terminal window one for Django project and another one for Django 
	background scheduler.

	In first terminal run: python manage.py runserver
	In second terminal run: python manage.py process_tasks


Database:

	There three table.
	
	1. Customer
	2. Payment Details
	3. Background Task
