from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUSer(AbstractUser):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=40)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10,
                                  blank=false,
                                  validators=[RegexValidator(r'^\d{10}$','Phone number must be of 10 digit')])
    
