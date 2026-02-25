from django.db import models

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
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='watches')

    def __str__(self):
        return self.name 