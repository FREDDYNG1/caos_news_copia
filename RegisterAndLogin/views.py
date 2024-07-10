from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import Reader, Writer
from .models import ReadUser, WriteUser


def userExist(username):
    return User.objects.filter(username=username).count() < 1

def register(request):
    if (request.method != 'POST'):
        return redirect('index')
    
    userType = request.POST["type"]
    context = {}
    
    if (request.POST["type"] == "write"):
        form = Writer()
        context = {
            'form':form,
            'user':userType
        }
        
        return render(request, "crearCuenta.html", context)
    
    elif (request.POST["type"] == "read"):
        form = Reader()
        context = {
            'form':form,
            'user':userType
        }
        
        return render(request, "crearCuenta.html", context)
        
    else:
        if (userType == "createwrite"):
            try:
                validate_email(request.POST['email'])
            except ValidationError:
                form = Writer()
                mensaje = 'Formato de email invalido'
                context = {
                    'form' : form,
                    'error' : mensaje,
                    'user' : 'write'
                }
                return render (request, 'crearCuenta.html', context)
            
            form = Writer(request.POST)
            if form.is_valid() and userExist(request.POST['userName']):
                
                form.save()
                
                user = User.objects.create_user(form.cleaned_data['userName'], form.cleaned_data['email'], request.POST['password'])
                user.first_name = "write"
                user.has_perm('RegisterAndLogin.view_Newspaper')
                user.has_perm('RegisterAndLogin.add_Newspaper')
                user.has_perm('RegisterAndLogin.dalate_Newspaper')
                user.has_perm('RegisterAndLogin.change_Newspaper')
                user.save()
                
                login(request, user)
                    
                form = Writer()
                return redirect('index')
            else:
                form = Writer()
                mensaje = 'los datos no son validos o el usuario ya esta registrado'
                context = {
                    'error': mensaje,
                    'form':form,
                    'user':'write'
                }
                return render(request, 'crearCuenta.html', context)
                    
        elif (userType == "createread"):
            try:
                validate_email(request.POST['email'])
            except ValidationError:
                form = Reader()
                mensaje = 'Formato de email invalido'
                context = {
                    'form' : form,
                    'error' : mensaje,
                    'user' : 'read'
                }
                return render (request, 'crearCuenta.html', context)
            
            form = Reader(request.POST)
            if form.is_valid() and userExist(request.POST['userName']):
                form.save()
                    
                user = User.objects.create_user(form.cleaned_data['userName'], form.cleaned_data['email'], form.cleaned_data['password'])
                user.first_name = "read"
                user.has_perm('RegisterAndLogin.view_Newspaper')
                
                form = Reader()
                return redirect('index')
            
            else:
                form = Reader()
                mensaje = 'los datos no son validos o el usuario ya esta registrado'
                context = {
                    'error': mensaje,
                    'form':form,
                    'user':'write'
                }
                return render(request, 'crearCuenta.html', context)
                

def tipoUser(request):

    if(request.method != "POST"):
        return render(request, "tipoUser.html")

def CambiarUsername(request):
    return render(request, 'cambiarUsername.html')

def cambiarPassword(request):
    return render(request, 'cambiarPassword.html');
    

def modelPassword(request):
    if (request.method == "POST"):
        user = request.user.username
        read = ReadUser.objects.all().filter(userName=user)
        write = WriteUser.objects.all().filter(userName=user)
        if (read):
            read.password = request.user.password
            read.save()
        elif (write):
            write.passwrod = request.user.password
            write.save()
        return redirect('index')
    else:
        return redirect('index')