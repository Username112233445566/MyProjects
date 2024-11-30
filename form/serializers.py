from rest_framework import serializers
from .models import Result, Form


class FormSerializers(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'


class ResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
