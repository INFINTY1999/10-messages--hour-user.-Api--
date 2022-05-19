from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('allmessage/', views.allmessages,name='allmessage'),
    path('createmessage/', views.createmessages,name='createmessage'),
    
    path('register/',views.registration,name='registration'),
    path('logout/', views.logout,name='logout'),    
    path('login/', obtain_auth_token,name='login'),
]
