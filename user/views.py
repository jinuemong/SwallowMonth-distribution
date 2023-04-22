from django.shortcuts import render
from .models import User,Profile
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny ,IsAuthenticated
from .serializers import LoginSerializer,ProfileSeralizer,RegstrationSerializer,UserSerializer
from rest_framework.response import Response
from .renderers import UserJsonRenderer #렌더 작업 전송 
from rest_framework import status ,filters 
from rest_framework.generics import RetrieveUpdateAPIView , RetrieveDestroyAPIView
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# 회원가입 view 
class RegistrationAPIView(APIView):
    
    # 누구나 허용 (회원가입)
    permission_classes = (AllowAny,)
    
    serializer_class = RegstrationSerializer
    renderer_classes = (UserJsonRenderer,)
    
    # 요청 
    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user) #직렬화
        serializer.is_valid(raise_exception=True) #유효성 확인 +예외처리
        user = serializer.save() # 저장
        ## 토큰 인증에는 object -모델을 전송해주어야 함 
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        # 성공 응답 반환
        return Response(
            {"user":serializer.data,
             "token":{
               "access":access_token,
               "refresh":refresh_token
             }
             },status=status.HTTP_201_CREATED)

# 로그인 view
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        # 요청 온 user를 serializer에 보내줌
        user = User.objects.get(userName=request.data["userName"])

        serializer = self.serializer_class(data=request.data) #직렬화
        serializer.is_valid(raise_exception=True) #유효성 확인 +예외처리

    
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            #유저 존재 시 성공 응답
            return Response(
                {"user":serializer.data,
                 "token":{
                "access":access_token,
                "refresh":refresh_token
                }
                },status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# 사용자 조회 + 업데이트
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView,RetrieveDestroyAPIView):
    
    # 인증 된 사용자만 접근 가능 
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = UserSerializer
    
    # 사용자 정보 조회
    def get(self,request,*args,**kwargs):
        
        #저장 없이 단순 반환 
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 부분 업데이트 
    def patch(self, request, *args, **kwargs):
        
        serializer_data = request.data
        
        # request.user -> instance
        # serializer_data -> validated_data
        # partial -> 부분 업데이트 옵션
        # serializer에 데이터 전달 후 리턴 받음 
        serializer = self.serializer_class(
            request.user,data=serializer_data,partial =True
        )
        
        serializer.is_valid(raise_exception=True)
        
        # 업데이트 정보 저장
        serializer.save()
        
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        user.delete()
        return Response(data, status=status.HTTP_200_OK)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSeralizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=userName__userName']
    #<참조하는 필드__참조 당하는 명>으로 해줘야 외래키 검색 가능



# profile & user 업데이트용

class UpdateProfileView(APIView):
    # 인증 된 사용자만 접근 가능 
    permission_classes = (IsAuthenticated,)
    
    def get_object(self,profileId):
        try:
            return Profile.objects.get(profileId = profileId)
        except Profile.DoesNotExist:
            return Response(id,status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        data = request.data #데이터 받기
        profile = self.get_object(data['profileId']) #이전 데이터 불러오기 
        serializer = ProfileSeralizer(profile,data=data) #새 데이터 적용 
    
        if serializer.is_valid(): 
            serializer.save() #데이터가 유효하면 저장 후 반환 
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class SearchUserView(APIView):
    def post(self,request):
        data = request.data
        data_list = Profile.objects.filter(
            userName__userName__icontains = data['search']
        )
        data_list = [ProfileSeralizer(put).data for put in data_list]
        return Response(data_list,status=status.HTTP_200_OK)