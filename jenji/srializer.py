from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Entry

class UserSerailizer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = "__all__"


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'