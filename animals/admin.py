from django.contrib import admin
from animals.models import Animal, UserProfile
from animals.models import UserProfile

class AnimalAdmin(admin.ModelAdmin): 
    list_display = ('name', 'species', 'breed', 'age', 'adopted')
    list_filter = ('species', 'adopted', 'sociable')
    search_fields = ('name', 'breed')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Animal, AnimalAdmin)
admin.site.register(UserProfile)