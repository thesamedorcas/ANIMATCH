from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


  #edit as you see fit
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    NAME_MAX_LENGTH = 128  # define max length
    name = models.CharField(max_length= NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
class Page(models.Model):
    TITLES_MAX_LENGTH = 128  # define max length
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLES_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title