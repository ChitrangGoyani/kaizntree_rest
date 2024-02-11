from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=12, default="NONE")
    tag = models.CharField(max_length=10, default="NONE")
    category = models.CharField(max_length=30, default="NONE")
    in_stock = models.IntegerField(default=0)
    stock_status = models.BooleanField(default=False)
    available_stock = models.IntegerField(default=0)