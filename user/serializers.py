from .models import User,Profile
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import authenticate,get_user_model

#serializer를 통해 사용자 등록을 위한 
# 요청(request)과 응답(response)을 직렬화(serialize)

# 등록 , 로그인, 유저 정보 serializer 생성

class RegstrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length = 128,
        min_length = 4,
        write_only = True
    )

    class Meta:
        model = User
        fields =[
            'userName',
            'password',
            ] 
        
    def create(self, validated_data):
        userName = validated_data['userName']
        if userName =='superuser':
            print("슈퍼 유저가 생성 되었습니다.",userName)
        
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)
        
    

# 사용자 로그인 
# username과 password를 확인 후 응답 전송

class LoginSerializer(serializers.Serializer):
    userName = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only = True)
    last_login = serializers.CharField(max_length=255,read_only = True)

    
    # 유효성 검사
    def validate(self, data):
        userName = data.get('userName',None)
        password = data.get('password',None)
        
        if userName is None:
            raise serializers.ValidationError(
                'An userName is required to log in!'
            )
            
        if password is None:
            raise serializers.ValidationError(
                'An password is required to log in!'
            )
            
        
        user = authenticate(userName=userName,password=password)
        
        #user data가 없다면 id , pw 오류
        
        if user is None:
            raise serializers.ValidationError(
                'An user with this userName and pw was not found'
            )
            
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )
            
        last_login = timezone.now()
        user.last_login = last_login
        user.save(update_fields=['last_login'])
        print("user auth",user.userName)
        return {
            'userName':user.userName,
            'last_login':user.last_login
        }
    

# 사용자 정보 확인 + 업데이트

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )    
    
    class Meta:
        model = User
        fields = [
            'userName',
            'password',
            'token'
        ]

        #토큰은 입력받을 필요가 없으므로
        # 따로 read_only_fields 속성을 줌
        read_only_fields = ('token', )
    
    # 사용자 업데이트
    
    def update(self,instance,validated_data):
        
        #pw는 django에서 자체적으로 함수 제공 
        # pop으로 pw 제거 *보안 강화
        password = validated_data.pop('password',None)
        
        for (key,value) in validated_data.items():
            setattr(instance,key,value)
                    
        # pw 수정
        if password is not None:
            instance.set_password(password)
            # set_password:  django 내부 pw 변환 함수
            
        instance.save()
        # instance는 객체 ex> user
        # db에 직접 저장하려면 save 호출
        return instance
    

class ProfileSeralizer(serializers.ModelSerializer):
    class Meta:
        managed = True
        model = Profile
        db_table = "Profiles"
        fields  = "__all__"
