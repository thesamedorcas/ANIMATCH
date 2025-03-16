from django.shortcuts import render
from django.http import HttpResponse
from animals.models import Category
from animals.models import Page
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from animals.forms import UserForm, UserProfileForm


def home(request):
    context_dict = {}
    context_dict['boldmessage'] = 'Welcome to ANIMATCH!'
    context_dict['categories'] = [] 
    context_dict['pages'] = []  
    
    visitor_cookie_handler(request)
    
    response = render(request, 'animals/home.html', context=context_dict)
    return response

def animals(request):
    context_dict = {}
    
    return render(request, 'animals/animals.html', context=context_dict)

@login_required
def recommended(request):
    context_dict = {}
    
    return render(request, 'animals/recommended.html', context=context_dict)

def signup(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
            
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('animals:home'))
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'animals/signup.html', 
                 context={'user_form': user_form, 
                          'profile_form': profile_form, 
                          'registered': registered})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('animals:home'))
            else:
                return HttpResponse("Your ANIMATCH account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'animals/login.html')

@login_required
def account(request):
    context_dict = {}
    
    return render(request, 'animals/account.html', context=context_dict)

@login_required
def animal_profile(request):
    context_dict = {}
    
    return render(request, 'animals/animal_profile.html', context=context_dict)

def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    return render(request, 'animals/about.html', context=context_dict)

def faq(request):
    return render(request, 'animals/faq.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('animals:home'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                              'last_visit',
                                              str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits
