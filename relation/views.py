from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import Profile
from user.serializers import ProfileSeralizer
from .models import FriendShip,FUser, Alarm , Message
from .Serializer import FrendShipSerializer,FUserSerializer,AlarmSerializer, MessageSerializer
from rest_framework import viewsets
from rest_framework import filters,status
import random

class FriendShipViewSet(viewsets.ModelViewSet):

    queryset  = FriendShip.objects.all()
    serializer_class = FrendShipSerializer
    filter_backends = [filters.SearchFilter]


class FUserViewSet(viewsets.ModelViewSet):

    queryset = FUser.objects.all()
    serializer_class = FUserSerializer
    filter_backends = [filters.SearchFilter]

class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all().order_by('createTime')
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=frId__frId']

def getFriendship(fromUser,targetUserId):
    
    findFromUser  = FUser.objects.filter(userId=fromUser)\
               &FUser.objects.filter(otherUser=targetUserId)
    findTargetUser= FUser.objects.filter(
        userId = Profile.objects.get(profileId=targetUserId).userName
    ) &         FUser.objects.filter(
        otherUser = Profile.objects.get(userName=fromUser).profileId
    )
    if findFromUser.exists() & findTargetUser.exists():
        frId = FUserSerializer(findFromUser[0]).data["frId"]
        return {"type":1,"frId":frId} # 친구
    elif findFromUser.exists() & ( not findTargetUser.exists() ):
        frId = FUserSerializer(findFromUser[0]).data["frId"]
        return {"type":2,"frId":frId} #요청 보냄
    elif (not findFromUser.exists() ) & findTargetUser.exists():
        frId = FUserSerializer(findTargetUser[0]).data["frId"]
        return {"type":3,"frId":frId} #요청 받음
    else:
        return {"type":4,"frId":None} #관계 없음 
    
class AlarmView(APIView):
    serializer_class = AlarmSerializer

    # userId type typeId -> 알림 중복 생성 방지 
    def post(self,request):
        data = request.data
        # 기존 데이터 유무 확인
        isData = Alarm.objects.filter(userId=data['userId'])\
        & Alarm.objects.filter(type=data['type'])\
        & Alarm.objects.filter(fromUserId=data['fromUserId']) # 보낸 유저 이름 
        if isData.exists():
            return Response(isData,status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    def get(self,request):
        data = request.query_params.get('userName')
        dataList = Alarm.objects.filter(userId=data)
        alarmList = []

        for alarm in dataList: # 상대 주체, 알림 내용을 전송
            alarmList.append({"profile":ProfileSeralizer(
                Profile.objects
                .get(userName = alarm.fromUserId))
                .data,"alarm":AlarmSerializer(alarm).data})
        return Response(alarmList,status=status.HTTP_200_OK)
    
    # def delete(self,request):
    #     data = request.data['alarmId']
    #     alarm = Alarm.objects.get(alarmId = data)
    #     try:
    #         alarm.delete()
    #         return Response(alarm,status=status.HTTP_200_OK)
    #     except alarm.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    

    

# 친구 리스트 (프로필 )
class FriendListView(APIView):

    def post(self,request):
        try:
            userName = request.data['userName']
            number = request.data['num']
            friendList = FUser.objects.filter(userId = userName)
            totalList  = []
        
            for friend in friendList: #친구 데이터 추가 
                targetUser = FUserSerializer(friend).data["otherUser"]
                relation = getFriendship(userName,targetUser)
        
                if relation["type"]==1:
                    totalList.append(ProfileSeralizer(Profile.objects.get(
                        profileId=friend.otherUser)).data)
            count = len(totalList)
            if number!="-1":
                return Response({"count":count,"friends":totalList[:int(number)]},status=status.HTTP_200_OK)
            return Response({"count":count,"friends":totalList},status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

# 랜덤유저 생성 
# userName을 받음 
class RandomUserView(APIView):

    def post(self,request):
        Profile_list = Profile.objects.all() # 전체 리스트 집합
        # 쿼리셋을 리스트로 변환 (profileId 추출 )
        Profile_list = [Profile_list[i].profileId for i in range(0,len(Profile_list))] 

        # 내  이름 
        pId = request.data['profileId']
        myProfile = Profile.objects.get(profileId = pId)
        # 내 친구 리스트 받기 
        put_list = FUser.objects.filter(userId = myProfile.userName)
        
        # 친구 리스트 profileId 추출   
        excludeList = set([put_list[i].otherUser for i in range(0,len(put_list))])
        # 제외 리스트에 나 추가 
        excludeList.add(int(pId))

        # 나와 친구가 아닌 리스트 얻기 
        profileList = [i for i in Profile_list if i not in excludeList]

        # 리스트가 10이하라면 n명 만큼 추출 
        rand_int = len(profileList) if len(profileList)<=10 else 10
        rand_list = random.sample(profileList,rand_int)

        # 랜덤 리스트를 프로필로 추출  
        randList = [ProfileSeralizer(Profile.objects.get(profileId=put))
                    .data for put in rand_list]

        return Response(randList,status=status.HTTP_200_OK)



# # 친구 리스트 (채팅방)
class MessageListView(APIView):

    def post(self,request):
        try:
            userName = request.data['userName']
            friendList = FUser.objects.filter(userName = userName)
            totalList = []
            # 두 데이터씩 받기 
            for friend in friendList:
                targetUser = FUserSerializer(friend).data["otherUser"]
                relation = getFriendship(userName,targetUser)
                if relation["type"]==1:
                    totalList.append([{"friendData":FrendShipSerializer(friend.frId).data,
                                       "profile":ProfileSeralizer(friend.otherUser).data }])
        
            return Response(totalList,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

## is frined? username ,targetUser (profile Id) 받음 
# 두 관계를 확인 (1. 친구관계, 2. 요청을 보낸 관계, 3. 요청을 받은 관계, 4. 아무런 관계 없음 )
class CheckFriendView(APIView):
    def post(self,request):
        try:
            userName = request.data['userName']
            targetUserId = request.data['targetUser'] #profileId
            return Response(getFriendship(userName,targetUserId),status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

                          