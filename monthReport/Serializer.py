from .models import MonthData, RecordData
from rest_framework import serializers
from task.Serializer import TaskSerializer
from routine.Serializer import  DayRoutineSerializer

class MonthDataSerializer(serializers.ModelSerializer):
    # taskPost = TaskSerializer(many=True,read_only=True)
    # dayRoutinePost = DayRoutineSerializer(many=True,read_only=True)
    
    # 갯수 카운터 
    taskCount = serializers.ReadOnlyField(source='taskPost.count')
    dayRoutineCount = serializers.ReadOnlyField(source='dayRoutinePost.count')
    class Meta:
        managed = True
        model = MonthData
        db_table = "MonthDatas"
        fields = ['monthId','userId','keyDate',
                  'totalPer','totalPoint',
                  'taskCount','dayRoutineCount',
                  'doneTask','clearRoutine']


class RecordDataSerializer(serializers.ModelSerializer):

    class Meta:
        managed = True
        model = RecordData
        db_table = "RecordDatas"
        fields = "__all__"

