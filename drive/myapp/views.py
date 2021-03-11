from django.shortcuts import render,redirect
from django.http import HttpResponse, FileResponse
import os
from drive.settings import BASE_DIR
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        folder_path = request.session['folder_location']
        data = os.listdir(folder_path)
        #print(data)
        file = []
        folder = []
        for i in data:
            loc = os.path.abspath(os.path.join(BASE_DIR,folder_path+"/{}".format(i)))
            #print(loc)
            lst = loc.split("/")
            #print(lst)
            main_path = lst[8:]
            #print(main_path)
            path = "/".join(str(e) for e in main_path)
            #print(path)
            if "." in i:
                dic = {
                    "name":i,
                    "location":loc
                }
                file.append(dic)
            else:
                dic = {
                    "name":i,
                    "location":path
                }
                folder.append(dic)
        
        context = {
            'file':file,
            'folder':folder,
            'folder_loc':folder_path
        }
        return render(request,'home.html',context=context)
    else:
        messages.error(request,"please Login")
        return redirect('signIn')
'''
def createfolder(request):
    #os.mkdir(os.path.join(BASE_DIR,'folders/myfolder3'))
    #lst = os.listdir(os.path.join(BASE_DIR,'folders'))
    #path = os.path.abspath(os.path.join(BASE_DIR,'folders/myfolder'))
    #os.mkdir(path+"/datafolder")
    return HttpResponse("Ok - {}".format(lst))
'''

def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request,"Account Exists")
            return redirect("signUp")
        user = User(username=username)
        user.set_password(password)
        user.save()
        folder = MyFolder(folder_name="{}_{}".format(user.username,user.id),user=user)
        folder.save()
        os.mkdir(os.path.join(BASE_DIR,'folders/{}'.format(folder.folder_name)))
        messages.success(request,"SignedUp")
        return redirect("signIn")
    else:
        return render(request,'signup.html')

def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request," Successfully logged in")
            folder = MyFolder.objects.get(user=user)
            request.session['folder_location'] = os.path.abspath(os.path.join(BASE_DIR,'folders/{}'.format(folder.folder_name)))
            print(request.session['folder_location'])
            return redirect("/")
        else:
            messages.error(request,"Credentials Error")
            return redirect("signIn")
    return render(request,'signin.html')


def logOut(request):
    auth.logout(request)
    messages.success(request,"LoggedOut")
    return redirect("/")


def fileDownload(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        print(location)
        file_name = location.split("/")[-1]
        file_to_download = open(str(location), 'rb')
        response = FileResponse(file_to_download, content_type='application/force-download')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file_name)
        return response


def uploadFile(request):
    if request.method == 'POST':
        location = request.POST.get("location")
        file = request.FILES.get("file")
        print(file)
        print(location)
        full_file = os.path.join(location,file.name)
        print(full_file)
        fout = open(full_file, 'wb+')
        file_content = ContentFile( request.FILES['file'].read() )
        # Iterate through the chunks.
        for chunk in file_content.chunks():
            fout.write(chunk)
        fout.close()
        lw = location.split("/")
        print(len(lw))
        lwi = lw[8:]
        nw = "-".join(str(e) for e in lwi)
        if len(lw)>8:
            return redirect('/myfolder/{}'.format(nw))
        else:
            return redirect('/')

def createFolder(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        #print(location)
        folder = request.POST.get('folder')
        os.mkdir(location+"/{}".format(folder))
        lw = location.split("/")
        lwi = lw[8:]
        nw = "-".join(str(e) for e in lwi)
        print(nw)
        if len(lw)>8:
            return redirect('/myfolder/{}'.format(nw))
        else:
            return redirect('/')

        
def myFolder(request):
    folder_path = request.POST.get("location")
    if request.method == 'POST':
        data = os.listdir(folder_path)
        #print(data)
        file = []
        folder = []
        for i in data:
            if "." in i:
                dic = {
                    "name":i,
                    "location":os.path.abspath(os.path.join(BASE_DIR,folder_path+"/{}".format(i)))
                }
                file.append(dic)
            else:
                dic = {
                    "name":i,
                    "location":os.path.abspath(os.path.join(BASE_DIR,folder_path+"/{}".format(i)))
                }
                folder.append(dic)
        
        context = {
            'file':file,
            'folder':folder,
            'cr_location':folder_path
        }
        return render(request,'myfolder.html',context=context)
    else:
        lst = folder_path.split("/")
        nw = lst[8:]
        path = '/'.join(str(e) for e in nw)
        print(path)
        return redirect("/myfolder/{}".format(path))


def viewFolder(request,path):
        path = path.replace('-','/')
        folder_path = request.session['folder_location']
        full_path = folder_path + "/" + path
        print(full_path)
        data = os.listdir(full_path)
        #print(data)
        file = []
        folder = []
        for i in data:
            loc = os.path.abspath(os.path.join(BASE_DIR,full_path+"/{}".format(i)))
            #print(loc)
            lst = loc.split("/")
            #print(lst)
            main_path = lst[8:]
            print("Actual Path",main_path)
            path = "-".join(str(e) for e in main_path)
            #print(path)
            if "." in i:
                dic = {
                    "name":i,
                    "location":loc
                }
                file.append(dic)
            else:
                dic = {
                    "name":i,
                    "location":path
                }
                folder.append(dic)
        
        context = {
            'file':file,
            'folder':folder,
            'folder_loc':full_path
        }
        return render(request,'myfolder.html',context=context)
    
