from rest_framework import serializers
from .models import Complain

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Complain
        fields = ("created_by","complain_title","complain_message","to_complain","complain_image")