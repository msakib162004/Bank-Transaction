# Generated by Django 3.2.12 on 2022-07-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.DecimalField(decimal_places=100, max_digits=100),
        ),
    ]
