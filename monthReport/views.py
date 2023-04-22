from django.shortcuts import render
from .models import MonthData , RecordData
from .Serializer import MonthDataSerializer , RecordDataSerializer
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,filters 

class MonthViewSet(viewsets.ModelViewSet):
    
    queryset = MonthData.objects.all()
    serializer_class = MonthDataSerializer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        userName= self.request.query_params.get('userName')
        keyDate = self.request.query_params.get('keyDate')
        # user + key data 검색 (1개 쿼리 반환)
        if userName and keyDate:
            queryset =self.queryset.filter(userId__userName  = userName) \
            & self.queryset.filter(keyDate = keyDate)     
            return queryset
        # user만 검색 (dayData리스트 반환)
        elif keyDate:
            queryset =self.queryset.filter(keyDate  = keyDate)
            return queryset
        # else
        return self.queryset
    

# 매 월 1일에 레코드 데이터 생성 : 해당 데이터의 순위 + 프로필 + MonthDate 생성
class RecordViewSet(viewsets.ModelViewSet):

    queryset = RecordData.objects.all()
    serializer_class = RecordDataSerializer
    filter_backends = [filters.SearchFilter]
    # search_fields = ['=userId__userName']

    def get_queryset(self):
        userName= self.request.query_params.get('userName')
        keyDate = self.request.query_params.get('keyDate')

        if userName and keyDate: # 가장 최근
            queryset = self.queryset.filter(userId__userName=userName).first()
            return queryset
        elif userName: # 유저의 레코드 
            queryset = self.queryset.filter(userId__userName=userName)
            return queryset
        
        return self.queryset

class RankingViewSet(viewsets.ModelViewSet):
    
    queryset = RecordData.objects.all()
    serializer_class = RecordDataSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=keyDate']