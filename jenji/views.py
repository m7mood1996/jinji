
# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .srializer import UserSerailizer, EntrySerializer
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import NewUser, Entry

from datetime import datetime, timedelta
import calendar



class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerailizer
    queryset = get_user_model().objects.all()
    
class EntryCreateView(APIView):
    queryset = get_user_model().objects.all()
    def post(self, request):
        print(request.user)
        adj_time = datetime.combine(datetime.today(), datetime.now().time()) + timedelta(hours=3)
        date = adj_time.strftime('%Y-%m-%d')
        time = adj_time.strftime('%H:%M')
        print(date)
        print(time)
        
        entry = Entry(user=request.user,
                      date =date,
                      time=time
                      )
        entry.save()
        # serializer = EntrySerializer(entry)
        # if serializer.is_valid():
            # serializer.save()
        return Response({}, status=201)
        # return Response(serializer.errors, status=400)
