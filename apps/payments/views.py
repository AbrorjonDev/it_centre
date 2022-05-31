from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

#local imports 
from .models import Group, GroupPayments
from .serializers import (
    GroupPaymentsPostSerializer,
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
        queryset = Group.objects.filter(created_by=user)
        if user and user.is_director:
            queryset += Group.objects.filter(created_by__created_by=user)
        elif user and user.is_admin:
            queryset += Group.objects.filter(created_by=user.created_by)
        elif user and user.is_superuser:
            queryset = Group.objects.all()
        return queryset.all()

    def get(self, request):
        queryset = self.get_queryset(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GroupDetailAPIView(APIView):
    """
    Retrieving, Editing and Deleting group object.

    in PATCH:
        name: str,
        cost: int,
        key: str,
        lessons_count: int
    """

    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        serializer = self.serializer_class(group,many=False)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        serializer = self.serializer_class(group,data=request.data,partial=True, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
        
    def delete(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        if group:
            group.delete()
            return Response({"detail":"Deleted succesfully"}, status=200)
        return Response({"detail":"Not found"}, status=400)



class GroupPaymentsAPIView(APIView):
    """
    Admins and directors can create payments here.
    In POST:
        full_name: str
        payment_amount: int (e.g. 400000)
        paid_admin: bool    (If you are an admin, this part will be accepted.)
        paid_director: bool     (If you are an director, this part will be accepted.)
        payment_date: Date  "YYYY-MM-DD"
        group: int     e.g. 1  --> Group object id
    """

    serializer_class = GroupPaymentsPostSerializer
    queryset = None
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class GroupPaymentsDetailAPIView(APIView):
    """
    Admins and directors can GET, PATCH, PUT, DELETE the payments.
    """

    serializer_class = GroupPaymentsSerializer
    queryset = None

    def get(self, request, pk):
        payment = get_object_or_404(GroupPayments, pk=pk)
        serializer = self.serializer_class(payment)
        return Response(serializer.data, status=200)
    
    def patch(self, request, pk):
        payment = get_object_or_404(GroupPayments, pk=pk)
        serializer = self.serializer_class(payment, data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        payment = get_object_or_404(GroupPayments, pk=pk)
        if payment:
            payment.delete()
            return Response({"detail":"deleted succesfully."}, status=200)
        return Response({"detail":"Not Found"}, status=404)

