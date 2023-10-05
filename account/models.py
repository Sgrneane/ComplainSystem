from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from main.models import ComplainName
from django.utils import timezone
from . import choices

# Creating Custom User Model
class CustomUser(AbstractUser):
    username=models.CharField(max_length=255,unique=False,null=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phone_number=models.CharField(max_length=10,
                                  blank=False,
                                  default=None,
                                  null=True,
                                  validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits')])
    created_date=models.DateTimeField(default=timezone.now)
    role = models.PositiveSmallIntegerField(choices=choices.ROLE_CHOICES, blank=True, null=False,default=3)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username',]
    
    
    def __str__(self) -> str:
        return self.email 
    def role_name(self):
        if self.role==1:
            return 'superadmin'
        elif self.role==2:
            return 'admin'
        else:
            return 'user'
    list_display = ["email",'first_name','last_name', "username",]


    
