# Generated by Django 4.1.3 on 2023-01-02 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_delete_retailer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=300)),
                ('open_time', models.CharField(max_length=300)),
                ('close_time', models.CharField(max_length=300)),
            ],
        ),
    ]
