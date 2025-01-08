from django.db import models

class CustomerData(models.Model):
    user_id = models.BigIntegerField(primary_key=True)  # int64 equivalent
    cust_name = models.CharField(max_length=255)  # object equivalent
    product_id = models.CharField(max_length=255)  # object equivalent
    gender = models.CharField(max_length=50)  # object equivalent
    age_group = models.CharField(max_length=50)  # object equivalent
    age = models.IntegerField()  # int64 equivalent
    marital_status = models.IntegerField()  # int64 equivalent
    state = models.CharField(max_length=255)  # object equivalent
    zone = models.CharField(max_length=100)  # object equivalent
    occupation = models.CharField(max_length=255)  # object equivalent
    product_category = models.CharField(max_length=255)  # object equivalent
    orders = models.IntegerField()  # int64 equivalent
    amount = models.FloatField(null=True, blank=True)  # float64 equivalent, nullable

    def __str__(self):
        return f"{self.user_id} - {self.cust_name}"
from django.db import models
class children(models.Model):
    name=models.CharField(max_length=100)
    SEX_CHOICES=[('M','Male'),('F','Female')]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age=models.IntegerField(null=True)
    def __str__(self):
        return self.name
class Message(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}: {self.content}'