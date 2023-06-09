# Generated by Django 4.1.3 on 2022-12-27 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_remove_order_status_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=255, null=True),
        ),
    ]
