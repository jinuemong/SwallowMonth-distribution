
from django.contrib.auth.models import BaseUserManager

# BaseUserManager : drf 내의 user를 생성할 때 사용하는 헬퍼 클래스
# create_user : user 생성
# create_superuser : 관리자 생성
# is_superuser, is_staff  -> True로 

class UserManager(BaseUserManager):
    
    def create_user(self,userName,password=None,**extra_fields):
        
        if userName is None:
            raise TypeError("Users must have userName!")
        
        if password is None:
            raise TypeError("Users must have password!")
        
        user = self.model(
            userName = userName,
            **extra_fields
        ) #pass는 생략 (감추기)
        
        # 대신 따로 제공하는 pw 함수 사용
        user.set_password(password)
        
        user.save() #저장
        
        return user #리턴 
    
    
    # admin user : superuser
    
    def create_superuser(self,userName,password, **extra_fields):
        
        if password is None:
            raise TypeError("Superuser must have password!")
        
        # create_user로 저장 후 superuser로 지정
        
        user = self.create_user(userName,password,**extra_fields)
        
        # superuser로 지정
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user
    
    