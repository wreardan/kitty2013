from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from core.models import *
from app import settings

import uuid
from boto.s3.connection import S3Connection
from boto.s3.key import Key
s3 = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_ACCESS_SECRET)
bucket = s3.create_bucket(settings.AWS_BUCKET_NAME)
bucket.set_acl('public-read')

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST.get('username'),
                                            password=request.POST.get('password'))
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/user/%d" % user.id)
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
           user_prof.cell_phone = request.POST['cell_phone']
           user_prof.save()
           new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
           auth.login(request, new_user)
           return HttpResponseRedirect('/user/%d' % new_user.id)
   else:
       form = UserCreationForm()
           
   context = {'form' : form}
   context.update(csrf(request))
   return render_to_response('registration/register.html', context)
   
@login_required
def add_meow(request):
    if request.method == "POST":
        newfile = request.FILES.get('new_meow_image')
        key = Key(bucket)
        keyname = str(int(uuid.uuid4()))[:10] + newfile.name
        key.key = keyname
        key.set_contents_from_string(newfile.read())
        key.make_public()
            
        url = 'https://s3.amazonaws.com/kitty2013/' + keyname

        user = request.user
        new_meow_text = request.POST.get('new_meow')
        new_meow = Meow(text=new_meow_text,
                        user=user, image_url=url)

        new_meow.save()

        # Find these values at https://twilio.com/user/account
        tagged_username = request.POST.get('tag')
        tagged_user = User.objects.filter(username=tagged_username)[0]
        if(tagged_user):
            cell = tagged_user.userprofile.cell_phone

            account_sid = "ACb65bbe159b7b180894c412cd4d47d231"
            auth_token = "19d4f44997dbabfb6b15add63408682f"
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.create(to="+%d" % cell, from_="+16083716550",
                    body="Hey %s, %s just tagged you in a picture" % (tagged_user.username, user.username))

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
def like_meow(request, meow_id):
    if request.method == "POST":
        meow = get_object_or_404(Meow, pk=meow_id)
        userprof = request.user.userprofile
        userprof.likes.add(meow)
        return redirect('/user/%s' % request.user.id)
    raise Http404

@login_required
def subscribe_user(request, user_id):
    if request.method == "POST":
        logged_user = request.user
        user = get_object_or_404(User, pk=user_id)
        user_prof = user.userprofile
        user_prof.followers.add(logged_user.userprofile)
        logged_user.userprofile.followers.add(user_prof)
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
        logged_user.userprofile.followers.remove(user_prof)
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

    suggestions = UserProfile.objects.all()

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

    for meow in meows:
        likes = user.userprofile.likes.all()
        if meow in likes:
            meow.liked = True
    
    context = {
        'meows': meows,
        'user_id': user_id,
        'logged_user': logged_user,
        'request': request,
        'same_user': same_user,
        'followers': followers,
        'following': following,
        'am_following': am_following,
		'suggestions': suggestions
    }
    context.update(csrf(request))
    return render_to_response('user_home.html', context)

@login_required
def user_upload(request, user_id):
    if request.method == "GET":
        context = {
            'user_id': user_id,
            'request': {'user': {'id' : user_id}},
        }
        context.update(csrf(request))
        return render_to_response('upload.html', context)
    if request.method == "POST":
        #TODO: post image
        return redirect('/upload/user/' + user_id)
    raise Http404