from django.db import models

# Create your models here.

class Category (models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Brand (models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Prodect (models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='prodents')
    image2 = models.ImageField(upload_to='prodents')
    image3 = models.ImageField(upload_to='prodents')
    image4 = models.ImageField(upload_to='prodents')
    description = models.TextField()
    price = models.DecimalField(max_digits=99999,decimal_places=2)
    old_price = models.DecimalField(max_digits=99999,decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.title

