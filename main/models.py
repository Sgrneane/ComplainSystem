from django.db import models
from django.conf import settings
from django.utils import timezone
from account.models import CustomUser
from django.db.models import QuerySet
from account import choices

# Create your models here.
class Complain(models.Model):
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_complains', on_delete=models.CASCADE)
    complain_title=models.CharField(max_length=255,null=False)
    complain_message=models.TextField(null=False)
    complain_image=models.ImageField(null=True, upload_to="Images")
    to_complain=models.CharField(choices=choices.ADMIN_CATEGORY, null=False,max_length=255)
    created_date=models.DateTimeField(default=timezone.now)
    

