from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transacao
from .form import TransacaoForm
import datetime


def home(request):
    data = {}
    data['transacoes'] = ['t1', 't2', 't3']

    data['now'] = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now
    return render(request, 'contas/home.html', data)

@login_required(login_url='/login/')
def listagem(request):
    data = {}
    data['transacoes'] = Transacao.objects.all()
    return render(request, 'contas/listagem.html', data)


def nova_transacao(request):
    data = {}
    form = TransacaoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_listagem')

    data['form'] = form
    return render(request, 'contas/form.html', data)


def update(request, pk):
    data = {}
    transacao = Transacao.objects.get(pk=pk)
    form = TransacaoForm(request.POST or None, instance=transacao)

    if form.is_valid():
        form.save()
        return redirect('url_listagem')

    data['form'] = form
    data['transacao'] = transacao
    return render(request, 'contas/form.html', data)


def delete(request, pk):
    transacao = Transacao.objects.get(pk=pk)
    transacao.delete()
    return redirect('url_listagem')


def login(request):
    data = {'now': datetime.datetime.now()}

    return render(request, 'contas/login.html', data)

@csrf_protect
def login_submit(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not  None:
            login(request, user)
            return redirect('/login/#')
        else:
            messages.error(request, 'Usuário ou senha inválido. Favor tentar novamente.')
        return redirect('/login/')
