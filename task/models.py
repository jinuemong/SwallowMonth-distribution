from django.db import models
from user.models import User
from monthReport.models import MonthData

class Task(models.Model):
    id = models.BigAutoField(primary_key=True,help_text="Task ID")
    monthId = models.ForeignKey(MonthData,on_delete=models.CASCADE
                                  ,related_name="taskPost",db_column='monthId',to_field='monthId')
    userId = models.ForeignKey(User,on_delete=models.CASCADE
                               ,related_name='taskPost',to_field='userName')
    dayIndex = models.IntegerField()
    text = models.TextField()
    isDone = models.BooleanField(default=False)
    iconType = models.IntegerField(default=0)
    level = models.IntegerField()
    per = models.IntegerField(default=0)
