# Generated by Django 4.1.3 on 2022-12-30 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_alter_status_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]