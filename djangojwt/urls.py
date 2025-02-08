from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Signup,Home,Login,UserList, UserDetail,Logout


urlpatterns = [
    path('',Signup.as_view(),name='signup'),
    path('login/',Login.as_view(),name="login"),
    path('logout/',Logout.as_view(),name="logout"),
    path('home/',Home.as_view(),name='home'),

    path('api/Userlist/',UserList.as_view()),
    path('api/Userlist/<int:pk>/',UserDetail.as_view()),

    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
]