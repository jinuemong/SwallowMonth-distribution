from user.models import User,Profile
from django.db import models
# two member
class FriendShip(models.Model):
    frId = models.BigAutoField(primary_key=True,help_text="Friendship ID")
    name = models.CharField(max_length=30,null=False)

class FUser(models.Model):
    fuId = models.BigAutoField(primary_key=True,help_text="FUser ID")
    frId = models.ForeignKey(FriendShip,on_delete=models.CASCADE
                             ,related_name="fUserPost",to_field="frId")
    userId = models.ForeignKey(User,on_delete=models.CASCADE
                               ,related_name="fUserPost",to_field="userName")
    otherUser = models.IntegerField(null=False)

# type으로 데이터 구분 typeId로 접근 
class Alarm(models.Model):
    alarmId = models.BigAutoField(primary_key=True,help_text="Alarm ID")
    userId = models.ForeignKey(User,on_delete=models.CASCADE
                               ,related_name="AlarmUserPost",to_field="userName")
    type = models.CharField(max_length=20,null=False)
    typeId = models.IntegerField(null=False)
    fromUserId = models.ForeignKey(User,on_delete=models.CASCADE
                                   ,related_name="AlarmFromUserPost",to_field="userName")
    isRead = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True) # 등록 시간 

class Message(models.Model):
    messageId = models.BigAutoField(primary_key=True,help_text="Message ID")
    frId = models.ForeignKey(FriendShip,on_delete=models.CASCADE
                             ,related_name="messagePost",to_field="frId")
    userId = models.ForeignKey(User,on_delete=models.CASCADE
                               ,related_name="messagePost",to_field="userName")
    isRead = models.BooleanField(default=False)
    text = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True) # 등록 시간 
