from django.db import models

class FoodOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer_name}, Item: {self.item_name}"
