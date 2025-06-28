from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='HomePage'),
    path('ExerciseForm', views.ExerciseForm, name='ExerciseForm'),
    path('ExercisePredict', views.ExercisePredict, name='ExercisePredict'),
    path('NutritionForm', views.NutritionForm, name='NutritionForm'),
    path('NutritionPredict', views.NutritionPredict, name='NutritionPredict'),
    path('DietForm', views.DietForm, name='DietForm'),
    path('DietPredict', views.DietPredict, name='DietPredict'),
    path('About', views.About, name='About'),
]