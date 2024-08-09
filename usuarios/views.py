from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages  import add_message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse

def cadastro(request):
    if request.method == 'GET':
        print('GET')
        return render(request, 'cadastro.html')
    elif request.method == 'POST':

        username = request.POST.get('username')
        senha  = request.POST.get('senha')
        confirmacao_senha = request.POST.get('confirmar_senha')
        print(senha)
        print(confirmacao_senha)

        if senha != confirmacao_senha:
            messages.add_message(request, messages.ERROR, 'Senhas não conferem')            
            return render(request, 'cadastro.html')
        
        if  len(senha) < 6:
            messages.add_message(request, messages.ERROR, 'Senha deve ter no mínimo 6 caracteres')
            return render(request, 'cadastro.html')
        
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Usuário já cadastrado')
            return render(request, 'cadastro.html')
        
        user = User.objects.create_user(username=username, password=senha)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso')
        return redirect(reverse('logar'))


def logar(request):
    if request.method == 'GET':
        return render(request, 'logar.html')
        
    elif request.method == 'POST':
         username = request.POST.get('username')
         senha = request.POST.get('senha')

         user = authenticate(username=username, password=senha)
         if user:
             
             login(request, user) 
             return redirect(reverse('cadastrar_empresa'))                     
            
         else:
             messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos')
             return render(request, 'logar.html')


def cadastrar_empresa(request):
    pass