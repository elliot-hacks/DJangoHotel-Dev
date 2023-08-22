from django.db import models
from django.core.validators import MinValueValidator
from .validators import validate_file_size


# Create your models here.
class Asset(models.Model):
    HOTEL_COUNTER = 'C'
    HOTEL_KITCHEN = 'K'
    HOTEL_ROOMS = 'R'
    HOTEL_CHOICES = [
        (HOTEL_COUNTER, 'COUNTER'),
        (HOTEL_KITCHEN, 'KITCHEN'),
        (HOTEL_ROOMS, 'ROOMS')
    ]
    asset = models.CharField(max_length=1, choices=HOTEL_CHOICES, default=HOTEL_COUNTER)
    
    def __str__(self) -> str:
        return self.asset

    class Meta:
        ordering = ['asset']


class Collection(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    #featured_product = models.ForeignKey(
    #    'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    images = models.ImageField(upload_to='uploads/', default='uploads/product.png', validators=[validate_file_size])
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    bought_at = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self) -> str:
        return f'{self.name}, {self.collection}, {self.price}'

    class Meta:
        ordering = ['name', 'collection', 'stock', 'price']


class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    PAYBY_CASH = 'CASH'
    PAYBY_MPESA = 'M-PESA'
    PAYBY_HALO = 'HALO-PESA'
    PAYBY_AIRTEL = 'AIRTEL-MONEY'
    PAYBY_TIGO = 'TIGO-PESA'
    PAYBY_NMB = 'NMB'
    PAYBY_CRDB = 'CRDB'
    PAYBY_KCB = 'KCB'
    PAYBY_PAYPAL = 'PAYPAL'
    PAYMENT_METHOD = [
    (PAYBY_CASH, 'CASH'),
    (PAYBY_MPESA, 'M-PESA'),
    (PAYBY_HALO, 'HALO-PESA'),
    (PAYBY_AIRTEL, 'AIRTEL-MONEY'),
    (PAYBY_TIGO, 'TIGO-PESA'),
    (PAYBY_NMB, 'NMB-BANK'),
    (PAYBY_CRDB, 'CRDB-BANK'),
    (PAYBY_KCB, 'KCB-BANK'),
    (PAYBY_PAYPAL, 'PAYPAL')
    ]

    payment = models.CharField(max_length=15, choices=PAYMENT_METHOD, default=PAYBY_CASH)

    def __str__(self) -> str:
        return f"{self.product.price} {self.payment} {self.product.stock} {self.product.name}"


    class Meta:
        ordering = ['product']
