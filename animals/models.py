from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

    

class Animal(models.Model):
    SPECIES_CHOICES = [ #Animal types/species
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Rabbit', 'Rabbit'),
        ('Bird', 'Bird'),
        ('Other', 'Other'),
    ]
    
    SEX_CHOICES = [ #animal sex choices
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
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='adopted_animals')
    sociable = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        #Fixing logic issue on database
        super(Animal, self).save(*args, **kwargs)
        if not self.slug or self.slug.endswith('-None'):
            self.slug = slugify(f"{self.name}-{self.id}")
            super(Animal, self).save(update_fields=['slug'])
    
    def __str__(self):
        return self.name
    
#Working on Adoption requests and favourite
class AdoptionRequest(models.Model):
    STATUS_CHOICES= [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='adoption_requests')
    message = models.TextField()
    contact_phone = models.CharField(max_length=20, blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.animal.name} - {self.status}"

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='favourited_by')
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'animal')
        
    def __str__(self):
        return f"{self.user.username} - {self.animal.name}"
