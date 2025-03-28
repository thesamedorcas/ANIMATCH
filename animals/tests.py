from django.test import TestCase
from django.test import SimpleTestCase
import os
import re
import warnings
import importlib
from animals.forms import AnimalForm
from animals.models import Favourite
from django.urls import reverse, resolve
from django.conf import settings
from animals.models import Animal, UserProfile
from animals.views import about, home
from populate_animals import populate
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from animals.models import AdoptionRequest


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ProjectStructureTests(TestCase):
    def test_animatch_has_urls_module(self):
        """ Ensures urls.py exists for animals """
        module_exists = os.path.isfile(os.path.join(settings.BASE_DIR, 'animals', 'urls.py'))
        self.assertTrue(module_exists)

    def test_is_animatch_app_configured(self):
        """ Checks if animals app exists """
        self.assertIn('animals', settings.INSTALLED_APPS)

class HomePageTests(TestCase):
    def setUp(self):
        populate()
        self.response = self.client.get(reverse('animals:home'))

    def test_home_uses_template(self):
        """ Verifies that the homepage view renders the correct template"""
        self.assertTemplateUsed(self.response, 'animals/home.html')

    def test_home_contains_correct_text(self):
        """ Checks that the homepage contains relevant text """
        self.assertContains(self.response, "Welcome to ANIMATCH")

class AboutPageTests(TestCase):
    def test_about_page_loads(self):
        """  Verifies that the about page loads successfully and contains the text """
        response = self.client.get(reverse('animals:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Who We Are")

class FormTests(TestCase):
    def test_animal_form_valid_data(self):
        """ Ensures that the AnimalForm is valid when provided with valid data for an animal """
        form = AnimalForm(data={
            'name': 'Buddy', 'species': 'Dog', 'breed': 'Labrador',
            'age': 3, 'sex': 'Male', 'about': 'Very friendly',
            'sociable': True, 'adopted': False
        })
        self.assertTrue(form.is_valid())

    def test_animal_form_missing_fields(self):
        """ Verifies that the AnimalForm is invalid when required fields are missing from the form data. """
        form = AnimalForm(data={})
        self.assertFalse(form.is_valid())

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user, website='http://example.com')
    
    def test_user_profile_creation(self):
        """ 
        Confirms that a UserProfile is correctly created when a user is created, 
        and that the profile is linked to the correct user. 
    
        """
        self.assertEqual(self.profile.user.username, 'testuser')
    
    def test_user_profile_str(self):
        """ 
        Verifies that the string representation of a UserProfile 
        instance returns the correct username. 
        """
        self.assertEqual(str(self.profile), 'testuser')
    
    def test_user_profile_update(self):
        """ 
        Tests the ability to update the UserProfile's website field, 
        ensuring the profile's data can be changed and saved. 
        """
        self.profile.website = 'http://newsite.com'
        self.profile.save()
        self.assertEqual(UserProfile.objects.get(user=self.user).website, 'http://newsite.com')

class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_valid_user(self):
        """ 
        Tests that a user can log in successfully with valid credentials 
        """
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

    def test_login_invalid_user(self):
        """ 
        Verifies that login fails when incorrect credentials are used
        """
        login = self.client.login(username='wronguser', password='wrongpassword')
        self.assertFalse(login)

class AnimalModelTest(TestCase):
    def setUp(self):
        # Creating a user for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        
    def test_animal_slug_creation(self):
        """  
        Ensures that the slug for an Animal is automatically created based on the 
        animal's name and ID when it is saved to the database.      
        """        
        animal = Animal.objects.create(
                    name='Test Animal',
                    species='Dog',
                    breed='Labrador',
                    age=2,
                    sex='Male',
                    about='A friendly dog.',
                    owner=self.user
                )
        animal.refresh_from_db()
        self.assertTrue(animal.slug)
        self.assertEqual(animal.slug, 'test-animal-{}'.format(animal.id))
    
    def test_animal_str_method(self):
        """
        Tests the string representation of an Animal instance, 
        verifying that it returns the animal's name.        
        """
        animal = Animal.objects.create(
                    name='Test Animal',
                    species='Dog',
                    breed='Labrador',
                    age=2,
                    sex='Male',
                    about='A friendly dog.',
                    owner=self.user
                )
                
        self.assertEqual(str(animal), 'Test Animal')
            
    def test_animal_save_creates_slug(self):
        """  
        Verifies that when a new Animal is created, 
        the slug field is populated with a valid slug. 
        """
        animal = Animal.objects.create(
            name="Buddy", 
            species="Dog", 
            breed="Labrador", 
            age=2, 
            sex="Female", 
            about="A playful dog.", 
            adopted=False,
            owner=None,
            sociable=True
        )
        self.assertIsNotNone(animal.slug)  # Check if slug is auto-generated

class AnimalFormTests(TestCase):
    
    def test_animal_form_valid_data(self):
        """ 
        Verifies that the AnimalForm is valid when provided with 
        the correct input data for an animal (name, species, age, etc.). 
        """
        form_data = {
            'name': 'Buddy',
            'species': 'Dog',
            'breed': 'Labrador',
            'age': 2,
            'sex': 'Male',
            'about': 'A friendly dog.',
            'sociable': True,
        }
        form = AnimalForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if the form is valid with proper data
       
    def test_animal_form_missing_name(self):
        """
        Test that an animal form is invalid if the name field is missing.
        """
        form_data = {
            'species': 'Dog',
            'breed': 'Labrador',
            'age': 2,
            'sex': 'Male',
            'about': 'A friendly dog.',
        }
        form = AnimalForm(data=form_data)
        self.assertFalse(form.is_valid(), "Form should be invalid when 'name' is missing.")

     
class AnimalViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.animal = Animal.objects.create(
            name="Buddy",
            species="Dog",
            breed="Labrador",
            age=2,
            sex="Male",
            about="A friendly dog",
            adopted=False,
            owner=self.user,
            sociable=True,
            slug="buddy-1"
        )
    
    def test_animal_profile_view(self):
        """ 
        Ensures that the profile page for an animal can be accessed, 
        verifying that the correct animal's name and "about" information are displayed on the page.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('animals:animal_profile', kwargs={'animal_id': self.animal.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.animal.name)  
        self.assertContains(response, self.animal.about) 
    
class URLTests(SimpleTestCase):
    def test_home_url_resolves(self):
        """ 
        Verifies that the URL for the homepage resolves to the correct view function.
        """
        url = reverse('animals:home')
        self.assertEqual(resolve(url).func, home)

    def test_about_url_resolves(self):
        """ 
        Confirms that the URL for the about page resolves to the correct view function. 
        """
        url = reverse('animals:about')
        self.assertEqual(resolve(url).func, about)

class FavouriteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.animal = Animal.objects.create(
            name="Buddy", 
            species="Dog", 
            breed="Labrador", 
            age=2, 
            sex="Male", 
            about="A friendly dog", 
            adopted=False,
            owner=None,
            sociable=True,
            slug="buddy-1"
        )
    
    def test_add_to_favourites(self):
        """ 
        Tests that a user can successfully add an 
        animal to their list of favourites.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('animals:add_favourite', kwargs={'animal_id': self.animal.id}))
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Favourite.objects.exists()) 

    def test_duplicate_favourite(self):
        """
        Verifies that a user cannot add the same animal to their favourites more than once. 
        It raises an exception if the duplicate entry is attempted.
        """
        Favourite.objects.create(user=self.user, animal=self.animal)
        with self.assertRaises(Exception):
            Favourite.objects.create(user=self.user, animal=self.animal)

    def test_favourite_str(self):
        """ 
        Verifies that the string representation of 
        a Favourite instance returns the correct format.
        """
        fav = Favourite.objects.create(user=self.user, animal=self.animal)
        expected_str = f"{self.user.username} - {self.animal.name}"
        self.assertEqual(str(fav), expected_str)

class AdoptionRequestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.animal = Animal.objects.create(
            name="Buddy", 
            species="Dog", 
            breed="Labrador", 
            age=2, 
            sex="Male", 
            about="A friendly dog", 
            adopted=False,
            owner=None,
            sociable=True,
            slug="buddy-1"
        )
    
    def test_create_adoption_request(self):
        """ 
        Ensures that a user can create an adoption request for an animal. 
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('animals:request_adoption', kwargs={'animal_id': self.animal.id}), 
                                    {'message': 'I love this dog!', 'contact_phone': '1234567890'})
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(AdoptionRequest.objects.exists()) 

class PermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='password')
        self.other_user = User.objects.create_user(username='other_user', password='password')
        self.animal = Animal.objects.create(
            name='Buddy', species='Dog', breed='Labrador', age=2, sex='Male', about='A friendly dog', owner=self.owner
        )

    def test_non_owner_cannot_edit_animal(self):
        """
        Verifies that a non-owner user cannot edit an animal's information.
        """
        self.client.login(username='other_user', password='password')
        response = self.client.post(reverse('animals:edit_animal', kwargs={'animal_id': self.animal.id}),
                                    {'name': 'New Name'})
        self.assertEqual(response.status_code, 403) 

    def test_non_owner_cannot_delete_animal(self):
        """
        Verifies that a non-owner user cannot delete an animal's information.
 
        """
        self.client.login(username='other_user', password='password')
        response = self.client.post(reverse('animals:delete_animal', kwargs={'animal_id': self.animal.id}))
        self.assertEqual(response.status_code, 403)

class EdgeCaseTests(TestCase):
    def test_animal_with_long_name(self):
        """ 
        Verifies that an animal can have a name that exceeds typical length constraints.
        """
        long_name = 'A' * 300  
        animal = Animal.objects.create(name=long_name, species='Dog', breed='Unknown', age=5, sex='Male', about='Test')
        self.assertEqual(animal.name, long_name)

    def test_special_characters_in_slug(self):
        """ 
        Ensures that animal names with special characters are correctly handled when generating slugs.
        """
        animal = Animal.objects.create(name='Test@Animal!2023', species='Dog', breed='Unknown', age=5, sex='Male', about='Test')
        self.assertIn('test-animal-2023', animal.slug)

class ConcurrencyTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.animal = Animal.objects.create(name='Buddy', species='Dog', breed='Labrador', age=2, sex='Male', about='A friendly dog', adopted=False)

    def test_two_users_trying_to_adopt_same_animal(self):
        """
        Verifies that when two users attempt to adopt the same animal at the same time, the animal is only adopted by the first user who requests adoption.
        """
        self.client.login(username='user1', password='password')
        response1 = self.client.post(reverse('animals:request_adoption', kwargs={'animal_id': self.animal.id}), {'message': 'I love this dog!', 'contact_phone': '1234567890'})
        
        self.client.login(username='user2', password='password')
        response2 = self.client.post(reverse('animals:request_adoption', kwargs={'animal_id': self.animal.id}), {'message': 'I also want this dog!', 'contact_phone': '0987654321'})
        
        self.animal.refresh_from_db()
        self.assertTrue(self.animal.adopted)  
        self.assertEqual(AdoptionRequest.objects.count(), 1)  

class DatabaseIntegrityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.animal = Animal.objects.create(name='Buddy', species='Dog', breed='Labrador', age=2, sex='Male', about='A friendly dog')
        self.favourite = Favourite.objects.create(user=self.user, animal=self.animal)

    def test_deleting_animal_removes_favourites(self):
        """ 
        Verifies that when an animal is deleted from the database, 
        all related favourite records are also deleted. 
        """
        self.animal.delete()
        self.assertFalse(Favourite.objects.filter(animal=self.animal).exists()) 

    def test_deleting_user_removes_favourites(self):
        """
        Ensures that when a user is deleted from the database, all favourite records associated with that user are also deleted.
        """
        self.user.delete()
        self.assertFalse(Favourite.objects.filter(user=self.user).exists())
