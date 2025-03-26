import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animatch.settings')
import django
django.setup()
from animals.models import Animal, Favorite, AdoptionRequest
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
import random
from django.template.defaultfilters import slugify

def populate():
    #commenting this out cos i think it's the problem
   # Animal.objects.all().delete()
    #creating tests cos I'm lost so i'm using randomizers

    admin_user = User.objects.get_or_create(username='admin')[0]
    user1 = User.objects.get_or_create(username='user1')[0]
    user2 = User.objects.get_or_create(username='user2')[0]

    users = [admin_user, user1, user2]

    animals = [
        {
            'name': 'Rex',
            'species': 'Dog',
            'breed': 'Staffy',
            'age': 14,
            'sex': 'Male',
            'about': 'Generic Story',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Anabell',
            'species': 'Dog',
            'breed': 'Bulldog',
            'age': 3,
            'sex': 'Female',
            'about': 'Generic Story',
            'sociable': False,
            'adopted': False
        },
        {
            'name': 'Rory',
            'species': 'Cat',
            'breed': 'Siamese',
            'age': 2,
            'sex': 'Male',
            'about': 'Generic Story',
            'sociable': False,
            'adopted': False
        },
        {
            'name': 'Generic name2',
            'species': 'Generic species',
            'breed': 'Generic breed',
            'age': 30,
            'sex': 'Generic Sex',
            'about': 'Generic Story',
            'sociable': False,
            'adopted': False
        },
        {
            'name': 'Generic name1',
            'species': 'Generic species',
            'breed': 'Generic breed',
            'age': 1037,
            'sex': 'Generic Sex',
            'about': 'Generic Story',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Generic name3',
            'species':'Generic species',
            'breed': 'Generic breed',
            'age':26678,
            'sex': 'Male',
            'about': 'Generic Story',
            'sociable': True,
            'adopted': True,
             
        }
    ]

    # Adding each animal
    created_animals = []
    for animal_data in animals:
        owner= random.choice(users)
        animal= create_animal(
            animal_data['name'],
            animal_data['species'],
            animal_data['breed'],
            animal_data['age'],
            animal_data['sex'],
            animal_data['about'],
            animal_data['sociable'],
            animal_data['adopted'],
            owner
        )
        created_animals.append(animal)

        creating_sample_favorites(users, created_animals)
        create_sample_requests(users, created_animals)
       
    
    # Printing all the animals 
    for a in Animal.objects.all():
        print(f"- {a.name}: {a.species}, {a.breed}, {'Adopted' if a.adopted else 'Available'}")

def create_animal(name, species, breed, age, sex, about, sociable=True, adopted=False, owner= None):
    #I figured out one issue was using kind because I had different functions with the same name, add_animal was replicated

    a, created = Animal.objects.get_or_create(
        name=name,
        defaults={
            'species': species,
            'breed': breed,
            'age': age,
            'sex': sex,
            'about': about,
            'sociable': sociable,
            'adopted': adopted,
            'owner' : owner, #another issue was i was using the old script before the existence of my owner variable
          
        }
    )
    
    
    if not created:
        a.species = species
        a.breed = breed
        a.age = age
        a.sex = sex
        a.about = about
        a.sociable = sociable
        a.adopted = adopted
        a.owner = owner # The same issue here, I lacked the owner variable
        a.save()

        
        
    return a
#I'm still testing to fix the issue with the database

def creating_sample_favorites(users, animals):
    
    Favorite.objects.all().delete()
 
    for user in users:
        num_favorites = random.randint(1, 2)
        for _ in range(num_favorites):
            animal = random.choice(animals)
     
            if animal.owner != user:
                Favorite.objects.get_or_create(user=user, animal=animal)
                print(f"User {user.username} favorited {animal.name}")  
def create_sample_requests(users, animals):
   
    AdoptionRequest.objects.all().delete()
    

    for _ in range(4):
        user = random.choice(users)
        
        available_animals = [a for a in animals if a.owner != user and not a.adopted]
        
        if available_animals:
            animal = random.choice(available_animals)
            status = random.choice(['pending', 'approved', 'rejected'])
            
            AdoptionRequest.objects.create(
                user=user,
                animal=animal,
                message=f"I would love to adopt {animal.name}",
                contact_phone=f"0-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                status=status
            )
            print(f"Created adoption request: {user.username} for {animal.name} ({status})")
    

if __name__ == '__main__':
    print('Starting the ANIMATCH population script...')
    populate()
