from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from animals.models import Animal, Favourite, UserProfile, AdoptionRequest, Favourite
from django.shortcuts import get_object_or_404
from django.contrib import messages
from animals.forms import UserForm, UserProfileForm, SignUpForm, AdoptionRequest, UserProfileEditForm, FavouriteForm, AdoptionRequestForm

def home(request):
    animal_list = Animal.objects.filter(adopted=False)[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Welcome to ANIMATCH!'
    context_dict['animals'] = animal_list
    
    
    visitor_cookie_handler(request)
    
    response = render(request, 'animals/home.html', context=context_dict)
    return response

def animals(request):
    #i changed some things for filters
    species = request.GET.get('species', '')
    breed = request.GET.get('breed', '')
    sex = request.GET.get('sex', '')
    sociable = request.GET.get('sociable', '')
    age_min = request.GET.get('age_min', '')
    age_max = request.GET.get('age_max', '')

    available_animals = Animal.objects.filter(adopted=False)
    filter_applied = False
    
    if species:
        available_animals = available_animals.filter(species=species)
        filter_applied = True
        
    if breed:
        available_animals = available_animals.filter(breed__icontains=breed)
        filter_applied = True
        
    if sex:
        available_animals = available_animals.filter(sex=sex)
        filter_applied = True
        
    if sociable:
        sociable_bool = sociable == 'True'
        available_animals = available_animals.filter(sociable=sociable_bool)
        filter_applied = True
        
    if age_min:
        available_animals = available_animals.filter(age__gte=int(age_min))
        filter_applied = True
        
    if age_max:
        available_animals = available_animals.filter(age__lte=int(age_max))
        filter_applied = True
    
    
    
    context_dict = {
        'animals': available_animals,
        'filter_applied': filter_applied,
        'species_choices': Animal.SPECIES_CHOICES,
        'sex_choices': Animal.SEX_CHOICES,}
    return render(request, 'animals/animals.html', context=context_dict)

@login_required
def recommended(request):
    user_favourites = Favourite.objects.filter(user=request.user)
    if user_favourites.exists():
        favourite_species = [fav.animal.species for fav in user_favourites]
        recommended_animals = Animal.objects.filter(
            species__in=favourite_species,
            adopted=False
        ).exclude(
            id__in=[fav.animal.id for fav in user_favourites]
        )[:10]
    else:
        recommended_animals = Animal.objects.filter(adopted=False).order_by('?')[:10]
    
    context_dict = {
        'recommended_animals': recommended_animals,
    }
    
    return render(request, 'animals/recommended.html', context=context_dict)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() 
            UserProfile.objects.create(user=user) #created cos i wanna save user in the database
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"Welcome to animatch, {username}!")
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
                messages.success(request, f"Welcome back to Animatch, {username}!")  
                return redirect(reverse('animals:home'))
            else:
                #using the messages message thing of design, apparently google says it's prettier and also jsut for page rendering
                messages.error(request, "Your ANIMATCH account is disabled.")
                return render(request, 'animals/login.html')
        else:
            messages.error(request, "Invalid login details supplied.")
            return render(request, 'animals/login.html')
    else:
        return render(request, 'animals/login.html')

@login_required
def account(request):
    favourites = Favourite.objects.filter(user=request.user)
    my_animals = Animal.objects.filter(owner=request.user)
    adoption_requests = AdoptionRequest.objects.filter(
        animal__owner=request.user
    ).order_by('-date_submitted')
    user_adoption_requests = AdoptionRequest.objects.filter(
        user=request.user
    ).order_by('-date_submitted')
    #temporary admin check we can change this to user later if you want
    is_admin = request.user.username in ['dorcas', 'euan', 'machan', 'andrea', 'arman']
    
    context_dict = {

        'favourites': favourites,
        'my_animals': my_animals,
        'is_admin': is_admin,
        'user_adoption_requests': user_adoption_requests,
        'species_choices': Animal.SPECIES_CHOICES,
        'sex_choices': Animal.SEX_CHOICES,
    }
    if is_admin:
        adoption_requests = AdoptionRequest.objects.all().order_by('-date_submitted')
        context_dict['adoption_requests'] = adoption_requests
    
    return render(request, 'animals/account.html', context=context_dict)

@login_required
def animal_profile(request, animal_id):
    try:
        animal = Animal.objects.get(id=animal_id)

        #Trying to stop the loop allowing users constantly request
        is_favourite = False
        existing_request = None 
        if request.user.is_authenticated:
            is_favourite = Favourite.objects.filter(user=request.user, animal=animal).exists()
        existing_request = AdoptionRequest.objects.filter( 
                user=request.user,
                animal=animal
            ).first()

        is_admin = request.user.username in ['dorcas', 'euan', 'machan', 'andrea', 'arman']


        context_dict = {
            'animal': animal,
            'is_favourite': is_favourite,
            'species_choices': Animal.SPECIES_CHOICES,
            'sex_choices': Animal.SEX_CHOICES,
            'existing_request': existing_request,
            'is_admin': is_admin,
        }


        return render(request, 'animals/animal_profile.html', context=context_dict)

        
        
    except Animal.DoesNotExist:
        messages.error(request, "The animal you are currently looking for does not exist.")
        return redirect('animals:animals')
    
          
    
@login_required
def request_adoption(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)


    if animal.adopted:
        messages.error(request, f"{animal.name} has already been adopted.")
        return redirect('animals:animal_profile', animal_id=animal_id)
    

    if request.user == animal.owner:
        messages.error(request, "You cannot adopt your own animal.")
        return redirect('animals:animal_profile', animal_id=animal_id)
    
    existing_request = AdoptionRequest.objects.filter(
        user=request.user,
        animal=animal,
        
    ).first()
    
    if existing_request:
        if existing_request.status == 'pending':
            messages.warning(request, f"You already have a pending adoption request for {animal.name}.")
        elif existing_request.status == 'approved':
            messages.success(request, f"Your request to adopt {animal.name} has been approved!")
        elif existing_request.status == 'rejected':
            messages.error(request, f"Your request to adopt {animal.name} was previously rejected.")
        return redirect('animals:animal_profile', animal_id=animal_id)
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user
            adoption_request.animal = animal
            adoption_request.status = 'Pending' #Fix for adoption request issue
            adoption_request.save()
            
            messages.success(request, f"Congratulations! You've submitted an adoption request for {animal.name}.")
            return redirect('animals:animal_profile', animal_id=animal_id)
    else:
        form = AdoptionRequestForm()
    
    return render(request, 'animals/request_adoption.html', {'form': form, 'animal': animal})

    
@login_required
def add_favourite(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    favourite, created = Favourite.objects.get_or_create(user=request.user, animal=animal)  
    if created:
        messages.success(request, f"{animal.name} has been added to your favourites!")
    else:
        messages.info(request, f"{animal.name} is already in your favourites.")
    return redirect('animals:animal_profile', animal_id=animal_id)

@login_required
def remove_favourite(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)    
    try:
        favourite = Favourite.objects.get(user=request.user, animal=animal)
        favourite.delete()
        messages.success(request, f"{animal.name} has been removed from your favourites.")
    except Favourite.DoesNotExist:
        messages.error(request, f"{animal.name} is not in your favourites.")

    if request.META.get('HTTP_REFERER') and 'account' in request.META.get('HTTP_REFERER'):
        return redirect('animals:account')
    else:
        return redirect('animals:animal_profile', animal_id=animal_id)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email', '')
        request.user.save()
        profile = request.user.userprofile
        profile.website = request.POST.get('website', '')
        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']

        
        profile.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('animals:account')
    
    return redirect('animals:account')

@login_required
def add_animal(request):
    if request.method == 'POST':
        try:
            animal = Animal()
            animal.name = request.POST.get('name')
            animal.species = request.POST.get('species')
            animal.breed = request.POST.get('breed')
            animal.age = request.POST.get('age')
            animal.sex = request.POST.get('sex')
            animal.about = request.POST.get('about')
            animal.sociable = request.POST.get('sociable') == 'True'
            animal.owner = request.user

            if 'picture' in request.FILES:
                animal.picture = request.FILES['picture']
            
            animal.save()
            #my peronal test for ids and names
            print(f"Animal added: {animal.name} (ID: {animal.id})")
            messages.success(request, f"Animal '{animal.name}' added successfully!")
            return redirect('animals:animal_profile', animal_id=animal.id)
        except Exception as e:
            messages.error(request, f"Error adding animal: {e}")
            return redirect('animals:account')
    return redirect('animals:account')

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
    messages.success(request, "You have successfully logged out.")
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

@login_required
def edit_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    if request.user != animal.owner and not request.user.is_superuser:
        messages.error(request, "You can only edit your own animals.")
        return redirect('animals:animal_profile', animal_id=animal_id)
    
    if request.method == 'POST':
        animal.name = request.POST.get('name')
        animal.species = request.POST.get('species')
        animal.breed = request.POST.get('breed')
        animal.age = request.POST.get('age')
        animal.sex = request.POST.get('sex')
        animal.about = request.POST.get('about')
        animal.sociable = request.POST.get('sociable') == 'True'
        
        
        if 'picture' in request.FILES:
            animal.picture = request.FILES['picture']
        
        animal.save()
        
        messages.success(request, f"{animal.name}'s details have been updated successfully!")
        return redirect('animals:animal_profile', animal_id=animal_id)
    
    return redirect('animals:animal_profile', animal_id=animal_id)

@login_required
def mark_adopted(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    
    #I did this for admins, if we decide to change it this is very important to change
    if request.user != animal.owner and not request.user.is_superuser:
        messages.error(request, "You can only mark your own animals")
        return redirect('animals:animal_profile', animal_id=animal_id)
    
    animal.adopted = True
    animal.save()
    
    messages.success(request, f"{animal.name} has been marked as adopted!") 
    return redirect('animals:animal_profile', animal_id=animal_id)
@login_required
def mark_available(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    if request.user != animal.owner and not request.user.is_superuser:
        messages.error(request, "You can only update your own animals.")
        return redirect('animals:animal_profile', animal_id=animal_id)
    
    animal.adopted = False
    animal.save()
    
    messages.success(request, f"{animal.name} has been marked as available")
    return redirect('animals:animal_profile', animal_id=animal_id)

@login_required
def process_adoption(request, request_id, status):
    if request.user.username not in [ 'euan', 'machan', 'andrea', 'arman', 'dorcas']:
        messages.error(request, "You don't have permission to process adoption requests, gerroutttt brooo.")
        return redirect('animals:account')   
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    adoption_request.status = status
    adoption_request.save()
    if status == 'approved':
        animal = adoption_request.animal
        animal.adopted = True
        animal.owner = adoption_request.user
        animal.save()
        
        messages.success(request, f"Adoption request for {animal.name} has been approved.")
    else:
        messages.info(request, f"Adoption request for {adoption_request.animal.name} has been rejected.")
    
    return redirect('animals:account')

#Adding a remove animal/delete the animal button

@login_required
def delete_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    is_admin = request.user.username in ['dorcas', 'euan', 'machan', 'andrea', 'arman']
    
    if request.user != animal.owner and not is_admin and not request.user.is_superuser:
        messages.error(request, "You are only allowed to delete your own animals.")
        return redirect('animals:animal_profile', animal_id=animal_id)  
    animal_name = animal.name
    animal.delete()
    
    messages.success(request, f"{animal_name} has been removed from the database")
    return redirect('animals:animals')