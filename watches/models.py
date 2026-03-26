from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


CATEGORY_CHOICES = [
    ('Luxury', 'Luxury'),
    ('Sport', 'Sport'),
    ('Casual', 'Casual'),
    ('Smart', 'Smart'),
    ('Vintage', 'Vintage'),
]

GENDER_CHOICES = [
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Unisex', 'Unisex'),
]


class Watch(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    description = models.TextField()
    image = models.ImageField(upload_to='watches')

    def __str__(self):
        return self.name


# ---------------------------
# Customer Model
# ---------------------------
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.name


# ---------------------------
# Optional separate Product model
# ---------------------------
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('Luxury', 'Luxury'),
        ('Sport', 'Sport'),
        ('Casual', 'Casual'),
        ('Smart', 'Smart'),
        ('Vintage', 'Vintage'),
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    price = models.FloatField()
    discounted_price = models.FloatField()

    description = models.TextField()
    image = models.ImageField(upload_to='watches')

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    mobile = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Mobile number must be exactly 10 digits",
            )
        ],
    )

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        if self.watch.discounted_price:
            return self.quantity * self.watch.discounted_price
        return self.quantity * self.watch.price

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'watch')

    def __str__(self):
        return f"{self.user.username} - {self.watch.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # total amount for this line item (kept for analytics / easier queries)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default="Pending")

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"
