from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='usuarios:login')
def solicitar_exames(request):
    # if not request.user.is_authenticated:
    #     #pode colorar um redirect
    #     return HttpResponse("Voçe deve fazer login para acessar esta pagina")
    if request.method == 'GET':
        return render(request, 'solicitar_exames.html')