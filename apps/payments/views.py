from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

#local imports 
from .models import Group, GroupPayments
from .serializers import (
    GroupPaymentsSerializer, 
    GroupSerializer
    )

class GroupAPIView(APIView):
    """
    Admins and directors create new groups, and get all datas about their groups.
    if you are a superuser, you can get all groups infos in db.

    in POST:
        name: str(100),
        cost: int, (e.g. 400000) (Optional)
        key: str (Optional field),
        lessons_count: int (Optional for now),
    """

    serializer_class = GroupSerializer

    def get_queryset(self, user=None):
        if user and user.is_director:
            queryset = Group.objects.filter(created_by=user)
            queryset += Group.objects.filter(created_by__created_by=user)
            return queryset
        return Group.objects.all()

    def get(self, request):
        pass




class GroupDetailAPIView(APIView):
    """
    Retrieving, Editing and Deleting group object.

    in PATCH:
        name: str,
        cost: int,
        key: str,
        lessons_count: int
    """

    serializer_class = None
    queryset = Group.objects.all()

    def get(self, request, pk):
        pass

    def patch(self, request, pk):
        pass


    def delete(self, request, pk):
        pass
    
