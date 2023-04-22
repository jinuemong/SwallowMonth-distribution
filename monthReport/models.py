from django.db import models
from user.models import User
# Create your models here.

class MonthData(models.Model):
    monthId = models.BigAutoField(primary_key=True,help_text="month ID")
    userId = models.ForeignKey(User,on_delete=models.CASCADE
                               ,related_name='monthPost',to_field='userName')
    keyDate = models.CharField(max_length=20,null=False)
    totalPer = models.IntegerField()
    totalPoint = models.IntegerField()
    doneTask = models.IntegerField()
    clearRoutine = models.IntegerField()


# 매 월 1일에 랭킹 데이터 생성 : 해당 데이터의 순위 + 프로필 + MonthDate 생성
# 전체 데이터를 순서대로 저장  -> 랭킹 데이터로 사용 
class RecordData(models.Model):
    recordId = models.BigAutoField(primary_key=True,help_text="record ID")
    ranking = models.IntegerField()
    userId = models.ForeignKey(User,on_delete=models.CASCADE
                               ,related_name='recordPost',to_field='userName')
    keyDate = models.CharField(max_length=20,null=False)
    totalPer = models.IntegerField()
    totalPoint = models.IntegerField()
    activityNum = models.IntegerField()
    clearNum = models.IntegerField()
# class RankingDate(models.Model): 
# rankingId , keyDate, totalUser(참가유저)
# class RankingUser(models.Model):
# rankingUserId , rankingId(forgin), ranking : 순위 , userId, monthId 
