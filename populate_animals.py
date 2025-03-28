import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animatch.settings')
import django
django.setup()
from animals.models import Animal, Favourite, AdoptionRequest
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
import random
from django.template.defaultfilters import slugify

def populate():
    # Clear all existing data
    # Animal.objects.all().delete()
    # Favourite.objects.all().delete()
    # AdoptionRequest.objects.all().delete()

    media_dir = os.path.join(os.getcwd(), 'media', 'animal_images')
    if not os.path.exists(media_dir):
        print(f"Media directory not found: {media_dir}")
        return

    # Mapping of animal names to image filenames
    animal_images = {
        'Rex': 'Rex.jpeg',
        'Anabell': 'Anabell.jpeg',
        'Rory': 'Rory.jpeg',
        'Bella': 'Bella.jpeg',
        'Max': 'Max.jpeg',
        'Charlie': 'Charlie.jpeg',
        'Luna': 'Luna.jpeg',
        'Buddy': 'Buddy.jpeg',
        'Cleo': 'Cleo.jpeg',
        'Daisy': 'Daisy.jpeg',
        'Oscar': 'Oscar.jpeg',
        'Milo': 'Milo.jpeg',
    }

    admin_user = User.objects.get_or_create(username='admin')[0]
    user1 = User.objects.get_or_create(username='user1')[0]
    user2 = User.objects.get_or_create(username='user2')[0]

    users = [admin_user, user1, user2]

    animals = [
        {
            'name': 'Rex',
            'species': 'Dog',
            'breed': 'Staffy',
            'age': 11,
            'sex': 'Male',
            'about': 'A loyal and friendly dog who loves to play fetch.',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Anabell',
            'species': 'Dog',
            'breed': 'Bulldog',
            'age': 3,
            'sex': 'Female',
            'about': 'A calm and affectionate dog who enjoys playing in the mud.',
            'sociable': False,
            'adopted': False
        },
        {
            'name': 'Rory',
            'species': 'Cat',
            'breed': 'Siamese',
            'age': 2,
            'sex': 'Male',
            'about': 'A curious and playful cat who loves attention.',
            'sociable': False,
            'adopted': False
        },
        {
            'name': 'Bella',
            'species': 'Rabbit',
            'breed': 'Lop',
            'age': 1,
            'sex': 'Female',
            'about': 'A gentle and quiet rabbit who enjoys being petted.',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Max',
            'species': 'Bird',
            'breed': 'African Grey',
            'age': 5,
            'sex': 'Male',
            'about': 'A talkative and intelligent parrot who loves company.',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Charlie',
            'species': 'Rodent',
            'breed': 'Golden Hamster',
            'age': 1,
            'sex': 'Male',
            'about': 'A small and energetic hamster who loves to explore.',
            'sociable': True,
            'adopted': True
        },
        {
            'name': 'Luna',
            'species': 'Cat',
            'breed': 'Persian',
            'age': 4,
            'sex': 'Female',
            'about': 'A fluffy and affectionate cat who enjoys lounging in the sun.',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Buddy',
            'species': 'Dog',
            'breed': 'Golden Retriever',
            'age': 6,
            'sex': 'Male',
            'about': 'A friendly and energetic dog who loves swimming.',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Cleo',
            'species': 'Reptile',
            'breed': 'Bearded Dragon',
            'age': 3,
            'sex': 'Female',
            'about': 'A calm and curious bearded dragon who enjoys basking in the sun.',
            'sociable': False,
            'adopted': False
        },
        {
            'name': 'Daisy',
            'species': 'Rabbit',
            'breed': 'Dutch Rabbit',
            'age': 2,
            'sex': 'Female',
            'about': 'A playful and energetic rabbit who loves hopping around.',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Oscar',
            'species': 'Bird',
            'breed': 'Parrakeet',
            'age': 1,
            'sex': 'Male',
            'about': 'A cheerful and whistling bird who loves attention.',
            'sociable': True,
            'adopted': False
        },
        {
            'name': 'Milo',
            'species': 'Rodent',
            'breed': 'Guinea Pig',
            'age': 2,
            'sex': 'Male',
            'about': 'A sociable and squeaky guinea pig who loves fresh veggies.',
            'sociable': True,
            'adopted': False
        }
    ]

    # Adding each animal
    created_animals = []
    for animal_data in animals:
        owner = random.choice(users)
        animal = create_animal(
            animal_data['name'],
            animal_data['species'],
            animal_data['breed'],
            animal_data['age'],
            animal_data['sex'],
            animal_data['about'],
            animal_data['sociable'],
            animal_data['adopted'],
            owner,
            animal_images.get(animal_data['name'])  # Get the image filename
        )
        created_animals.append(animal)

        
    
    # Printing all the animals
    for a in Animal.objects.all():
        print(f"- {a.name}: {a.species}, {a.breed}, {'Adopted' if a.adopted else 'Available'}")


def create_animal(name, species, breed, age, sex, about, sociable=True, adopted=False, owner=None, image_filename=None):
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
            'owner': owner,
        }
    )

    if not created:
        # Update fields if the animal already exists
        a.species = species
        a.breed = breed
        a.age = age
        a.sex = sex
        a.about = about
        a.sociable = sociable
        a.adopted = adopted
        a.owner = owner

    # Attach the image only if it doesn't already exist
    if image_filename and not a.picture:
        image_path = os.path.join(os.getcwd(), 'media', 'animal_images', image_filename)
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                a.picture.save(image_filename, ImageFile(image_file), save=True)

    a.save()
    return a

if __name__ == '__main__':
    print('Starting the ANIMATCH population script...')
    populate()
