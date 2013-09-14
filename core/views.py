from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from core.models import *

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST.get('username'),
                                            password=request.POST.get('password'))
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/user/%s" % user.id)
    context = {}
    context.update(csrf(request))
    return render_to_response( 'registration/login.html',  context)

def register(request):
   if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
           new_user = form.save()
           new_user.save()
           return HttpResponseRedirect('/accounts/login')
   else:
       form = UserCreationForm()
           
   context = {'form' : form}
   context.update(csrf(request))
   return render_to_response('registration/register.html', context)
   
@login_required  
def user_home(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        new_meow_text = request.POST.get('new_meow')
        new_meow = Meow(text=new_meow_text,
                        user=user)
        new_meow.save()
        return redirect('/user/%s' % user.id)
    else:
        meows = user.meow_set.all()
        context = {
            'meows': meows,
            'request': request
        }
        context.update(csrf(request))
        return render_to_response('user_home.html', context)