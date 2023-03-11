from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    # brand = models.CharField(max_length=250, default='unbranded')
    retailer = models.ForeignKey(
        User, related_name='product', limit_choices_to={'groups__name': "retailer"}, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    quantity = models.PositiveBigIntegerField(default=10)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])
