from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from blog.models import *

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')



class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ('id','title','content','date_publish')

    
