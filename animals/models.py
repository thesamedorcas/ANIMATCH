import time
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.user.username


class Animal(models.Model):
    SPECIES_CHOICES = [ #i wasn't sure what to put, so you can chnage this
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Rabbit', 'Rabbit'),
        ('Bird', 'Bird'),
        ('Other', 'Other'),
    ]
    
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    name = models.CharField(max_length=128)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=128)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    about = models.TextField()
    picture = models.ImageField(upload_to='animal_images', blank=True)
    adopted = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='adopted_animals')
    sociable = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if  self.id:
            #if animal has been save to database and have id, create unique slug
            self.slug = slugify(f"{self.name}-{self.id}")
            super(Animal, self).save(*args, **kwargs)
        else:
            #if animal does not have unique id, save with temp slug  made from name, time of request and users unique id,
            #then resave to create unique
            strtime = time.time()
            self.slug = slugify(f"{self.name}-{strtime}-{self.owner.id}")
            super(Animal, self).save(*args, **kwargs)
            self.save()




    def __str__(self):
        return self.name