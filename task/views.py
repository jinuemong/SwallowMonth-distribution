from django.shortcuts import render

from .models import Task
from .Serializer import  TaskSerializer
from rest_framework import viewsets
from rest_framework import filters 

            

class TaskViewSet(viewsets.ModelViewSet):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    
    def get_queryset(self):
        userName= self.request.query_params.get('userName')
        monthId = self.request.query_params.get('monthId')
        dayIndex = self.request.query_params.get('dayIndex')
        # user + key data 검색 >  이번달 리스트 뽑기 
        if userName and monthId:
            queryset =self.queryset.filter(userId__userName  = userName) \
            & self.queryset.filter(monthId  = monthId)     
            return queryset
        # user + key date + day 검색 > 하루 리스트 뽑기
        if userName and monthId and dayIndex:
            queryset =self.queryset.filter(userId__userName  = userName) \
            & self.queryset.filter(monthId  = monthId) & self.queryset.filter(dayIndex=dayIndex)
            return queryset
        # else
        return self.queryset