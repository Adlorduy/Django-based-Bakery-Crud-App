from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name

class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)

class Order(models.Model):
    date = models.DateField()
    entry_time = models.TimeField() 
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class DeliverySchedules(models.Model):
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

from django.db import models

class DeliveryVehicle(models.Model):
    delivery_person = models.ForeignKey('DeliveryPerson', on_delete=models.CASCADE)
    VEHICLE_CHOICES = [
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle'),
        ('bicycle', 'Bicycle'),
    ]
    vehicle = models.CharField(max_length=10, choices=VEHICLE_CHOICES)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.delivery_person} - {self.vehicle}'

    def clean(self):
        if self.vehicle == 'bicycle':
            self.license_number = None
            self.expiration_date = None


class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    product_image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total