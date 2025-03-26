import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animatch.settings')
import django
django.setup()
from animals.models import Animal
from django.core.files.images import ImageFile
import random
from django.template.defaultfilters import slugify

def populate():
    Animal.objects.all().delete()

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
            animal_data['sociable'],
            animal_data['adopted']
        )
    
    # Printing all the animals 
    for a in Animal.objects.all():
        print(f"- {a.name}: {a.species}, {a.breed}, {'Adopted' if a.adopted else 'Available'}")

def add_animal(name, species, breed, age, sex, about, sociable=True, adopted=False):
   
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
        a.save()
        
    return a

if __name__ == '__main__':
    print('Starting the ANIMATCH population script...')
    populate()