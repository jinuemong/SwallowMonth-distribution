from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        managed = True
        model = Task
        db_table = "Tasks"
        fields = "__all__"
