from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .forms import Reader, Writer, ChangePassword, ChangeUserName
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
                user.has_perm('RegisterAndLogin.delete_Newspaper')
                user.has_perm('RegisterAndLogin.change_Newspaper')
                user.has_perm('RegisterAndLogin.delete_WriteUser')
                user.has_perm('RegisterAndLogin.change_WriteUser')
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
                user.has_perm('RegisterAndLogin.delete_ReadUser')
                user.has_perm('RegisterAndLogin.change_ReadUser')
                
                login(request, user)
                
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
    if (request.method != 'POST'):
        form = ChangeUserName()
        context = {
            'form':form
        }
        return render(request, 'cambiarUsername.html', context)
    username = request.user.username
    typeUser = User.objects.filter(username=username).first().first_name
    newUsername = request.POST['newUsername']
    cNewUsername = request.POST['CnewUserName']
    
    if (User.objects.filter(username=newUsername).count() == 1):
        form = ChangeUserName()
        mensaje = 'usuario ya registrado'
        context = {
            'form':form,
            'error':mensaje
        }
        return render(request, 'cambiarUsername.html', context)
    
    if (newUsername == cNewUsername):
        if (typeUser == 'write'):
            writeU = WriteUser.objects.get(userName=username)
            user = User.objects.get(username=username)
            writeU.userName = newUsername
            user.username = newUsername
            user.save()
            writeU.save()
            
            login(request, user)
            return redirect('index')
        elif (typeUser == 'read'):
            readU = ReadUser.objects.get(userName=username)
            user = User.obects.get(username=username)
            readU.userName = newUsername
            user.username = newUsername
            user.save()
            writeU.save()
            
            login(request, user)
            return redirect('index')
    else:
        form = ChangeUserName()
        mensaje = 'Los campos no coinciden'
        context = {
            'form':form,
            'error':mensaje
        }
        return render(request, 'cambiarUsername.html', context)
            
            
            


def oldPasswordCorrect(old, user):
    password = User.objects.filter(username=user).first().password
    print(password)
    return check_password(old, password)

def cambiarPassword(request):
    if (request.method != 'POST'):
        form = ChangePassword()
        context = {
            'form':form
        }
        return render(request, 'cambiarPassword.html', context);
    
    oldP = request.POST['oldPassword']
    newP = request.POST['newPassword']
    cNewP = request.POST['newPasswordC']
    username = request.user.username
    
    if (oldPasswordCorrect(oldP, username)):
        
        if (newP == cNewP):    
            user = User.objects.get(username=username)
            user.set_password(newP)
            user.save()
            login(request, user)
            return redirect('index')
        
        else:
            form = ChangePassword()
            mensaje = "los campos no coinciden"
            context = {
                'form':form,
                'error':mensaje
            }
            return render(request, 'cambiarPassword.html', context)
    else:
        form = ChangePassword()
        mensaje = "la contraseña antigua es incorrecta"
        context = {
            'form':form,
            'error':mensaje
        }
        return render(request, 'cambiarPassword.html', context)