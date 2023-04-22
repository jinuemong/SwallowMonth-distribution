
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.fields import BooleanField
from .managers import UserManager
from datetime import datetime, timedelta
import jwt

class User(AbstractBaseUser,PermissionsMixin):
    userName = models.CharField(max_length=255, unique=True,db_column='userName')
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    
    USERNAME_FIELD = "userName"  # 로그인 시 id로 사용
    
    objects = UserManager()
    
    def __str__(self):
        return self.userName
    
    # def get_full_name(self):
    #         return self.userName

    # def get_short_name(self):
    #     return self.userName
    
    
    # # 사용자 인증을 위한 토큰 생성
    # @property
    # def token(self):
    #     return self._generate_jwt_token()
    
    # # 토큰 발행 함수(자체)
    # def _generate_jwt_token(self):
    #     #다른 토큰 생성을 위한 시간 값  
    #     dt = datetime.now() + timedelta(days=60)
        
    #     token = jwt.encode({
    #         'id' : self.pk,
    #         'exp': dt.utcfromtimestamp(dt.timestamp())
            
    #         #hash를 통한 암호화
    #     }, settings.SECRET_KEY, algorithm = "HS256")
        
    #     return token 
    

class Profile(models.Model):
    profileId  = models.BigAutoField(primary_key=True,help_text="Profile ID")
    userName = models.OneToOneField(User,on_delete=models.CASCADE,db_column='userName',to_field='userName') 
    userImage = models.ImageField(default='default.png',upload_to="%Y/%m/%d")
    userComment = models.TextField(null=False,default="")
    
    # str 반환
    def __str__(self):
        return self.userName.userName