from django.contrib import admin
from .models import Complain, ComplainName,Response

# Register your models here.
admin.site.register(Complain)
admin.site.register(ComplainName)
admin.site.register(Response)
