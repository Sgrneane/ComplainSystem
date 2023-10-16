from django.db import models
from django.conf import settings


class Complain(models.Model):
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_complains', on_delete=models.CASCADE,default=None,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    complain_title=models.CharField(max_length=255,null=False)
    complain_message=models.TextField(null=False)
    complain_image=models.ImageField(null=True, upload_to="Images")
    to_complain=models.ForeignKey('ComplainName', on_delete=models.CASCADE)
    class Meta:
        ordering=['-created_date']

    def __str__(self):
        return self.complain_title
    
    
    
class ComplainName(models.Model):
    department_name = models.CharField(max_length=255,null=False)
    complain_name = models.CharField(max_length=255,null=False)

    def __str__(self):
        return self.complain_name
    
#Response Model
class Response(models.Model):
    response_to=models.OneToOneField(Complain, related_name="response", on_delete=models.CASCADE,default=None,null=True)
    response_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="responses",on_delete=models.CASCADE,null=True,default=None)
    response_body=models.TextField()
    response_image=models.ImageField(null=True,upload_to="Images")
    created_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_date']

