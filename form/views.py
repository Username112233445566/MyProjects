from django.shortcuts import render
from rest_framework import generics
from .models import Form, Result
from .serializers import FormSerializers, ResultSerializers
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import hashlib

class FormView(generics.ListAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializers


class ResultView(generics.CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializers

    def get_client_identifier(self, request, form_id):
        """
        Генерирует уникальный идентификатор клиента для конкретного опроса.
        """
        client_ip = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        identifier = f"{client_ip}-{user_agent}-{form_id}"  # Привязываем к ID опроса
        return hashlib.sha256(identifier.encode()).hexdigest()

    def create(self, request, *args, **kwargs):
        form_id = request.data.get("form")  # Получаем ID формы из данных запроса
        if not form_id:
            return Response({"detail": "ID опроса не указан."}, status=status.HTTP_400_BAD_REQUEST)

        client_identifier = self.get_client_identifier(request, form_id)
        if cache.get(client_identifier):  # Проверяем, заблокирован ли клиент для данного опроса
            return Response(
                {"detail": "Вы уже отправили ответ на этот опрос."},
                status=status.HTTP_403_FORBIDDEN,
            )
        response = super().create(request, *args, **kwargs)
        cache.set(client_identifier, True, timeout=3600 * 24)  # Блокируем на 24 часа
        return response


def survey(request):
    return render(request, 'survey.html')