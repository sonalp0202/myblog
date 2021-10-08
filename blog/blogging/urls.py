from django.urls import path
from .views import registeruser,activate


urlpatterns = [path('register/',registeruser,name='register'),
               path('activate/<uidb64>/<token>/',activate, name='activate')]