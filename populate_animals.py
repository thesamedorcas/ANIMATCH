import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animatch.settings')
import django
django.setup()
from animals.models import Animal
from django.core.files.images import ImageFile
from django.contrib.auth.models import User
import random
from django.template.defaultfilters import slugify

def populate():
    Animal.objects.all().delete()

    ##create two test users and assign to animals
    if User.objects.filter(username="genny").exists():
        genericUser1 = User.objects.get(username="genny")
        print("Genny exists, and collected\n")
    else:
        genericUser1 = User.objects.create_user("genny","genny.generic1@email.com","GennyIsNumberOne!!!")
        genericUser1.first_name = "Genny"
        genericUser1.last_name = "GenericUser1"
        genericUser1.save()
        print("Genny created")

    if User.objects.filter(username="omar").exists():
        genericUser2 = User.objects.get(username="omar")
        print("Omar exists, and collected\n")
    else:
        genericUser2 = User.objects.create_user("omar","omar.generic2@email.com","OmarIsNumberTwo:(")
        genericUser2.first_name = "Omar"
        genericUser2.last_name = "GenericUser2"
        genericUser2.save()
        print("Omar created")

    # load personal account and assign the animals 3,6
    try:
        tester_user = User.objects.get(username="machan")
    except:
        tester_user = genericUser1

    animals = [
        {
            'name': 'Rex',
            'species': 'Dog',
            'breed': 'Staffy',
            'age': 14,
            'sex': 'Male',
            'about': 'Generic Story',
            'owner':genericUser1,
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
            'owner':genericUser2,
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
            'owner':tester_user,
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
            'owner':genericUser1,
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
            'owner':genericUser2,
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
            'owner':tester_user,
            'sociable': True,
            'adopted': True  
        }
    ]
    
    # Adding each animal
    for animal_data in animals:
        add_animal(
            animal_data['name'],
            animal_data['species'],
            animal_data['breed'],
            animal_data['age'],
            animal_data['sex'],
            animal_data['about'],
            animal_data['owner'],
            animal_data['sociable'],
            animal_data['adopted']
        )
    
    # Printing all the animals 
    for a in Animal.objects.all():
        print(f"- {a.name}: {a.species}, {a.breed}, {a.owner}, {'Adopted' if a.adopted else 'Available'}")

def add_animal(name, species, breed, age, sex, about, owner, sociable=True, adopted=False):
   
    a, created = Animal.objects.get_or_create(
        name=name,
        defaults={
            'species': species,
            'breed': breed,
            'age': age,
            'sex': sex,
            'about': about,
            'owner': owner,
            'sociable': sociable,
            'adopted': adopted,
            'slug': slugify(name)  
        }
    )

    
    
    # if not created:
    #     a.species = species
    #     a.breed = breed
    #     a.age = age
    #     a.sex = sex
    #     a.about = about
    #     a.owner = owner
    #     a.sociable = sociable
    #     a.adopted = adopted
    #     a.save()

    a.species = species
    a.breed = breed
    a.age = age
    a.sex = sex
    a.about = about
    a.owner = owner
    a.sociable = sociable
    a.adopted = adopted
    a.save()
        
    return a

if __name__ == '__main__':
    print('Starting the ANIMATCH population script...')
    populate()