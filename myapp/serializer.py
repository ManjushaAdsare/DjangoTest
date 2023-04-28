from django.db import models
from rest_framework import serializers
from .models import Candidates


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidates
        fields = "__all__"