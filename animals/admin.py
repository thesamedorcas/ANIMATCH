from django.contrib import admin
from animals.models import Category, Page
from animals.models import UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin) 
admin.site.register(Page)
admin.site.register(UserProfile)