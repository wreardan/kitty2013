from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
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
           user_prof = UserProfile(user=new_user)
           user_prof.save()
           return HttpResponseRedirect('/accounts/login')
   else:
       form = UserCreationForm()
           
   context = {'form' : form}
   context.update(csrf(request))
   return render_to_response('registration/register.html', context)
   
@login_required
def add_meow(request):
    if request.method == "POST":
        user = request.user
        new_meow_text = request.POST.get('new_meow')
        new_meow = Meow(text=new_meow_text,
                        user=user)
        new_meow.save()
        return redirect('/user/%s' % user.id)
    raise Http404

@login_required
def remove_meow(request, meow_id):
    if request.method == "POST":
        user = request.user
        meow = get_object_or_404(Meow, pk=meow_id)
        if user != meow.user:
            raise Http404
        meow.delete()
        return redirect('/user/%s' % user.id)
    raise Http404

@login_required
def subscribe_user(request, user_id):
    if request.method == "POST":
        logged_user = request.user
        user = get_object_or_404(User, pk=user_id)
        user_prof = user.userprofile
        user_prof.followers.add(logged_user.userprofile)
        user_prof.save()
        return redirect('/user/%s' % user.id)   
    raise Http404
    
@login_required
def unsubscribe_user(request, user_id):
    if request.method == "POST":
        logged_user = request.user
        user = get_object_or_404(User, pk=user_id)
        user_prof = user.userprofile
        user_prof.followers.remove(logged_user.userprofile)
        user_prof.save()
        return redirect('/user/%s' % user.id)   
    raise Http404

@login_required  
def user_home(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    logged_user = request.user
    meows = []
    am_following = False
    
    followers = user.userprofile.followers.all()
    following = user.userprofile.userprofile_set.all()
    if logged_user == user:   
        same_user = True
        for f in following:
            meows.extend(f.user.meow_set.all())
    else :
        same_user = False
        if logged_user.userprofile in followers:
            am_following = True

    meows.extend(user.meow_set.all())
    meows.sort(key=lambda m: m.ts, reverse=True)
    
    context = {
        'meows': meows,
        'user_id': user_id,
        'logged_user': logged_user,
        'request': request,
        'same_user': same_user,
        'followers': followers,
        'following': following,
        'am_following': am_following
    }
    context.update(csrf(request))
    return render_to_response('user_home.html', context)
