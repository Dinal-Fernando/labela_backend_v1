from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


