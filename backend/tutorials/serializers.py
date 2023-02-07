from rest_framework import serializers
from tutorials.models import Tutorial
class TutorialSerilizer(serializers.ModelSerializer):
    class Meta:
        model= Tutorial
        fields=("id","question","answer")