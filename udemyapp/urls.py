from django.urls import path
from .views import  recommend_courses,course_recommendation_view

urlpatterns = [
    path('',recommend_courses, name='recommend_courses'),
path('course_recommendation_view/',course_recommendation_view,name='course_recommendation_view'),
]
