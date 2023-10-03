from django.shortcuts import (render, redirect)
from django.http import (HttpResponse)
from django.contrib.auth.models import (User)
# Create your views here.


def cadastro(request):

    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        # Captura o valor dos campos quando o metodo e POST
        # nome_var    = request.POST.get('atributo name= no html')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # TODO passar para um arquivo de utils 
        #Validaçoes de dados

        if not senha == confirmar_senha:
            return redirect('usuarios:cadastro')
        
        if len(senha) < 8:
            return redirect('usuarios:cadastro')
        
        if User.objects.filter(username=username).exists():
            return redirect('usuarios:cadastro')
        # TODO validar se o username do usuario não existe
        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = username,
                email = email,
                password = senha
            )
        except:
            return redirect('usuarios:cadastro')

        return HttpResponse('passou salvo ')