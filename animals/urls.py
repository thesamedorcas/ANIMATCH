from django.urls import path
from django.contrib.auth import urls
from animals import views

app_name = 'animals'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    # Authentication/login
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Account
    path('account/', views.account, name='account'),
    path('account/<int:animal_id>/', views.animal_profile, name='animal_profile'),
    path('account/add_animal/',views.add_animal,name='add_animal'),
    path('account/edit_animal/<int:animal_id>/',views.edit_animal,name='edit_animal'),

    # Animals
    path('animals/', views.animals, name='animals'),
    path('animals/recommended/', views.recommended, name='recommended'),

    # Help
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

   
]