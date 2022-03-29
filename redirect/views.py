from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
import json
from .models import Couplet
from .forms import *

# Create your views here.

def c7001667f5e7626138e9e4334f4a9766(request):
    logout(request)
    return redirect('index')
    
def e35e6da7bdbc4c0bec05f32bea5c6ae1(request):
    if request.method == 'POST':
        total_post = request.POST.get('dataPost', None)
        total_post = json.loads(total_post)
        add_post = total_post[0]
        merge = total_post[1]
        user_id = add_post[0]
        for precouplet in add_post[1]:
            in_url = precouplet[0]
            in_url = in_url.strip().lower()
            if in_url == '':
                raise
            out_url = precouplet[1]
            if user_id != -1:
                user = User.objects.get(id=user_id)
                couplet_query = Couplet.objects.filter(in_url=in_url)
                if len(couplet_query) == 1 and merge == True:
                    couplet = couplet_query[0]
                    couplet.user = user
                elif len(couplet_query) == 0:
                    couplet = Couplet(user=user, in_url=in_url, out_url=out_url)
                else:
                    raise
            else:
                couplet = Couplet(in_url=in_url, out_url=out_url) 
            couplet.save()
    return HttpResponse(status=200)
    
def ec8db41d74c36b954821ab64f8226de0(request):
    if request.method == 'POST':
        total_post = request.POST.get('dataPost', None)
        total_post = json.loads(total_post)
        in_url = total_post[0]
        merge = total_post[1]
        couplet_query = Couplet.objects.filter(in_url=in_url)
        if len(couplet_query) == 1:
            couplet = couplet_query[0]
            couplet.delete()
        else:
            raise
    return HttpResponse(status=200)

def index(request):

    popup = request.session.get('popup')
    if popup is None:
        popup = ''
    else:
        del request.session['popup']
        
    if request.user.is_authenticated:
        user_id = request.user.id
        userdisplay = request.user.profile.userdisplay
        if userdisplay is None:
            userdisplay = request.user.username
        register_form = ''
        login_form = ''
        couplet_list = [[couplet.in_url, couplet.out_url] for couplet in request.user.couplet_set.all()] 
    else:
        user_id = -1
        userdisplay = ''
        register_form = UserCreationForm()
        login_form = LoginForm()
        couplet_list = []
        if request.method == 'POST':
            if 'register_submit' in request.POST:
                register_form = UserCreationForm(request.POST)
                if register_form.is_valid():
                    register_form.save()
                    request.session['popup'] = 'registered'
                    user = authenticate(username = register_form.cleaned_data['username'],
                                        password = register_form.cleaned_data['password1'],
                                        )
                    login(request, user)
                    return redirect('index')
                popup = 'sign-up-button'
            
            if 'login_submit' in request.POST:
                login_form = LoginForm(request.POST)
                if login_form.is_valid():
                    user = login_form.cleaned_data
                    login(request, user)
                    return redirect('index')
                popup = 'sign-in-button'

    return render(request, 'redirect/index.html', {
        'user_id': user_id,
        'userdisplay': userdisplay,
        'register_form': register_form,
        'login_form': login_form,
        'popup': popup,
        'couplet_list': couplet_list,
    })
    
def redirecter(request, in_url):
    in_url = in_url.lower()
    couplet_query = Couplet.objects.filter(in_url=in_url)
    if len(couplet_query) == 1:
        couplet = couplet_query[0]
        try:
            return redirect(couplet.out_url)
        except:
            return HttpResponse('Something went wrong.')
    else:
        return HttpResponse('That url does not go anywhere.')
        
def terms_conditions(request):
	return render(request,'redirect/terms_conditions.html')
	
def privacy_policy(request):
	return render(request,'redirect/privacy_policy.html')
	
def cookies_policy(request):
	return render(request,'redirect/cookies_policy.html')

def robots(request):
	return render(request, 'redirect/robots.txt')

def sitemap(request):
	return render(request, 'redirect/sitemap.xml')
        
        
        
        
        
        
        
        
        
        
        
    
