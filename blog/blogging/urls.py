from django.urls import path
from .views import registeruserviaemail,activate


urlpatterns = [path('register/',registeruserviaemail,name='register'),
               path('activate/<uidb64>/<token>/',activate, name='activate')]