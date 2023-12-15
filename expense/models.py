from django.db import models



class Expense(models.Model):
    text = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    location = models.TextField()  # You can store the location details here
    created_at = models.DateTimeField(auto_now_add=True)

