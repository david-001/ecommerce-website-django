# Generated by Django 4.1.3 on 2022-12-27 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=300),
        ),
    ]
