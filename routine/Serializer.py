from .models import Routine, DayRoutine
from rest_framework import serializers


class DayRoutineSerializer(serializers.ModelSerializer):
    
    class Meta:
        managed = True
        model = DayRoutine
        db_table = "DayRoutines"
        fields = "__all__"
        
class RoutineSerializer(serializers.ModelSerializer):
    
    dayRoutinePost = DayRoutineSerializer(many = True, read_only = True)
    
    class Meta:
        managed = True
        model = Routine
        db_table = "Routines"
        fields = ['routineId','userId','monthId','keyDate','text','cycle','startNum',
                  'totalRoutine','clearRoutine','iconType','topText',
                  'dayRoutinePost']
        