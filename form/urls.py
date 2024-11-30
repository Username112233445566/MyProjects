from django.urls import path
from .views import FormView, ResultView, survey


urlpatterns = [
    path('form/', FormView.as_view(), name='form'),
    path('result/', ResultView.as_view(), name='result'),
    path('survey/', survey, name='survey'),
]