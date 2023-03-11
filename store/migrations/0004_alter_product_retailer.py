# Generated by Django 4.1.3 on 2022-12-29 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_remove_product_brand_product_retailer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='retailer',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'retailer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to=settings.AUTH_USER_MODEL),
        ),
    ]
