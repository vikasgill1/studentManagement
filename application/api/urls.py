from django.urls import path
from .views import *


urlpatterns = [
    path('register/',Register.as_view()),
    path('login/',LoginApiView.as_view()),
    path('profile/',ProfileView.as_view()),
    path('profileview',ProfileDataView.as_view()),
    path('forgetpassword/',ForgetPassword.as_view())
]
