from django.db import models
from django.core import serializers
from django.contrib.auth.models import User
import json

# Create your models here.
class MenuItem(models.Model):

    ITEM_TYPES = (
        ('Regular Pizza', 'Regular Pizza'),
        ('Sicilian Pizza', 'Sicilian Pizza'),
        ('Sub', 'Sub'),
        ('Pasta', 'Pasta'),
        ('Salad', 'Salad'),
        ('Dinner Platter', 'Dinner Platter')
    )
    type = models.CharField(max_length=64, choices=ITEM_TYPES)

    name = models.CharField(max_length=64, blank=True)

    takesExtras = models.BooleanField()

    isOneSize = models.BooleanField()

    singleSizeCost = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    smallCost = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    largeCost = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        if self.type in ("Regular Pizza", "Sicilian Pizza"):
            return self.pizza.__str__()
        else:
            return f"{self.name}"

    def extras_formatted(self):
        extras = [{"name": extra.name, "cost": extra.addedCost.__str__(), "has_cost": bool(extra.addedCost)} for extra in self.extras.all()]
        return json.dumps(extras);

    def price_formatted(self):
        if self.isOneSize:
            return self.singleSizeCost
        else:
            prices = {"small": self.smallCost.__str__(), "large": self.largeCost.__str__()}
            return json.dumps(prices)

    def price(self, size):
        if self.isOneSize:
            return self.singleSizeCost
        elif size == "small":
            return self.smallCost
        else:
            return self.largeCost

class Pizza(MenuItem):

    numberToppings = models.IntegerField()

    def __str__(self):
        if self.numberToppings == 0:
            return f"Cheese"
        else:
            return f"{self.numberToppings} Topping {self.type}"

class Extra(models.Model):

    name = models.CharField(max_length=64)

    addedCost = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    forItems = models.ManyToManyField(MenuItem, related_name="extras", limit_choices_to={"takesExtras": True})

    def __str__(self):
        if self.addedCost:
            return f"{self.name} (+{self.addedCost})"
        return f"{self.name}"

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    status = models.CharField(max_length=64, default="open")

    def __str__(self):
        return f"{self.pk} ({self.user}, {self.status})"


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    size = models.CharField(max_length=64, blank=True)

    cost = models.DecimalField(max_digits=4, decimal_places=2)

    extras = models.ManyToManyField(Extra)

    def __str__(self):
        return f"{self.order}: {self.item}, {self.size}"

    # Override save method
    def save(self, *args, **kwargs):
        # Calculate base cost of order based on size of item
        self.cost = self.item.price(self.size)
        # Save item
        super().save(*args, **kwargs)
