from django.db import models
from user.models import User
from monthReport.models import MonthData
class Routine(models.Model):
    routineId = models.BigAutoField(primary_key=True,help_text="Routine ID")
    userId = models.ForeignKey(User,on_delete=models.CASCADE
                               ,related_name='routinePost',to_field='userName')
    monthId = models.ForeignKey(MonthData,on_delete=models.CASCADE
                                  ,related_name="routinePost",db_column='monthId',to_field='monthId')
    keyDate = models.CharField(max_length=20,default=False)
    text = models.TextField()
    cycle = models.IntegerField()
    startNum = models.IntegerField()
    totalRoutine = models.IntegerField()
    clearRoutine = models.IntegerField()
    iconType = models.IntegerField(default=0)
    topText = models.CharField(max_length=50,default=False)


class DayRoutine(models.Model):
    id = models.BigAutoField(primary_key=True,help_text="DayRoutine ID")
    routineId = models.ForeignKey(Routine,on_delete=models.CASCADE
                                  ,related_name="dayRoutinePost",db_column='routineId',to_field='routineId')
    monthId = models.ForeignKey(MonthData,on_delete=models.CASCADE
                                  ,related_name="dayRoutinePost",db_column='monthId',to_field='monthId')
    dayIndex =  models.IntegerField()
    clear = models.BooleanField(default=False)