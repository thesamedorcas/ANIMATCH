from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from datetime import datetime
from animals.models import Animal
from animals.forms import AnimalForm, UserForm, UserProfileForm, SignUpForm

def home(request):
    animal_list = Animal.objects.filter(adopted=False)[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Welcome to ANIMATCH!'
    context_dict['animals'] = animal_list
    
    
    visitor_cookie_handler(request)
    
    response = render(request, 'animals/home.html', context=context_dict)
    return response

def animals(request):
    all_animals = Animal.objects.all()
    print(f"All animals: {all_animals}")
    available_animals = Animal.objects.filter(adopted=False)
    print(f"Available animals: {available_animals}")
    context_dict = {'animals': available_animals}
    return render(request, 'animals/animals.html', context=context_dict)

@login_required
def recommended(request):
    context_dict = {}
    
    return render(request, 'animals/recommended.html', context=context_dict)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('animals:home')
    else:
        form = SignUpForm()
    return render(request, 'animals/signup.html', {'form': form})

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
def animal_profile(request, animal_id):
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist:
        return redirect('animals:animals')
    
    if (request.user == animal.owner) :
        is_owner = True
    else:
        is_owner = False
    
    
    context_dict = {'animal': animal,
                    'is_owner':is_owner}
    
    return render(request, 'animals/animal_profile.html', context=context_dict)

@login_required
def add_animal(request):
    
    if request.method == "POST":

        form = AnimalForm(request.POST,request.FILES)
        #validate form
        if form.is_valid():
            #create animal with temporary slug, non unique
            animal = form.save(commit=False)
            animal.owner = request.user
            animal.save()
            return redirect('animals:account')

    context_dict = {'animal': Animal,
                    'form':AnimalForm(),
                    'is_owner':True,
                    'page_function':'add'}
    return render(request, 'animals/animal_profile.html', context=context_dict)
    
@login_required
def edit_animal(request, animal_id):
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist:
        return redirect('animals:animals')
    
    if (request.user == animal.owner) :
        is_owner = True
    else:
        is_owner = False

    #edit animal details if post request and is owner
    if (request.method == "POST") and is_owner:

        #check form is valid using animal instance
        animal = Animal.objects.get(id=animal_id)
        form = AnimalForm(request.POST,request.FILES,instance=animal)

        #if form valid save and commit changes and return to profile
        if form.is_valid():
            form.save()
            return redirect('animals:account')

    
    context_dict = {'animal': animal,
                    'form':AnimalForm(),
                    'is_owner':is_owner}
    
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
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

