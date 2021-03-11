from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    #path('createfolder',createfolder,name='createfolder'),
    path('signup',signUp,name='signUp'),
    path('signin',signIn,name='signIn'),
    path("logout",logOut,name="logOut"),
    path("downloadfile",fileDownload,name="filedownload"),
    path("createfolder",createFolder,name="createfolder"),
    path("uploadfile",uploadFile,name="uploadFile"),
    #path("myfolder",myFolder,name="myFolder"),
    path("myfolder/<path>",viewFolder,name='viewfolder')
]
