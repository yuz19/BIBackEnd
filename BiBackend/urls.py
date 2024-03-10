"""
URL configuration for Bi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import (analyse,connect_to_mysql,reconnect_to_mysql)
urlpatterns = [
    # path('student/', views.studentApi),
    # path('student/<int:pk>/', views.studentDetailApi),
    path('api/analyse/', analyse, name='analyse'),
    path('api/sql/', connect_to_mysql, name='mysql'),
    path('api/resql/', reconnect_to_mysql, name='remysql'),
    path('admin/', admin.site.urls),
]

