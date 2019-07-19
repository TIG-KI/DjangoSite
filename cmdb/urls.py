from django.contrib import admin
from django.urls import path
from cmdb import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="addUser"),
    path("addUser/",views.addUser,name="addUser"),
    path("disPUI/",views.UserList,name="UserList"),
    path("findMovie/",views.findMovie,name="find movie")
]
