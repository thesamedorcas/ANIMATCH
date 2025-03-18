from django.test import TestCase
import os
import re
import warnings
import importlib
from django.urls import reverse
from django.conf import settings
from animals.models import Category, Page
from populate_animals import populate
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ProjectStructureTests(TestCase):

    def test_animatch_has_urls_module(self):
            """
            Did you create a separate urls.py module for Animals?
            """
            module_exists = os.path.isfile(os.path.join(self.animals_app_dir, 'urls.py'))
            self.assertTrue(module_exists, f"{FAILURE_HEADER}The animals app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")
        

    def test_is_animatch_app_configured(self):
            """
            Did you add the new Animals app to your INSTALLED_APPS list?
            """
            is_app_configured = 'animals' in settings.INSTALLED_APPS
            
            self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The animals app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")
        

class HomePageTests(TestCase):
    """
    Testing the basics of homepage view and URL mapping.
    Also runs tests to check the response from the server.
    """
    def setUp(self):
        populate()
        self.content = self.response.content.decode()
        self.views_module = importlib.import_module('animals.views')
        self.views_module_listing = dir(self.views_module)
        self.response = self.client.get(reverse('animals:home'))
        self.project_urls_module = importlib.import_module('animatch.urls')

    def test_home_uses_template(self):
        """
        Checks whether the home view uses a template -- and the correct one!
        """
        self.assertTemplateUsed(self.response, 'animals/home.html', f"{FAILURE_HEADER}Your home() view does not use the expected home.html template.{FAILURE_FOOTER}")
    
    def test_home_uses_context_dictionary(self):
        """
        Tests whether the home view uses the context dictionary correctly.
        generic        
        """
        self.assertTrue('boldmessage' in self.response.context, f"{FAILURE_HEADER}In your home view, the context dictionary is not passing the boldmessage key. Check your context dictionary in the home() view, located in animals/views.py, and try again.{FAILURE_FOOTER}")
        
        message = self.response.context['boldmessage']
        expected = 'generic'
        self.assertEqual(message, expected,  f"{FAILURE_HEADER}The boldmessage being sent to the home.html template does not match what is expected. Check your home() view. Make sure you match up cases, and don't miss any punctuation! Even one missing character will cause the test to fail.{FAILURE_FOOTER}")
    
    def test_home_starts_with_doctype(self):
        """
        Is the <!DOCTYPE html> declaration on the first line of the home.html template?
        """
        self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your home.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
    
    def test_about_link_present(self):
        """
        Is the about hyperlink present and correct on the home.html template?
        """
        expected = "<a href=\"/animals/about/\">About</a><br />"
        self.assertTrue(expected in self.response.content.decode(), f"{FAILURE_HEADER}Your home.html template doesn't contain the /animals/about/ link -- or it is not correct. Make sure you have the linebreak in, too!{FAILURE_FOOTER}")
        

    
    def test_view_exists(self):
        """
        Does the home view exist in Animals's views.py module?
        """
        name_exists = 'home' in self.views_module_listing
        is_callable = callable(self.views_module.home)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The home view for Animals does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the home view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")
    
    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Animals's urls.py.
        """
        home_mapping_exists = False
        
        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'home':
                    home_mapping_exists = True
        
        self.assertTrue(home_mapping_exists, f"{FAILURE_HEADER}The home URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('animals:home'), '/animals/', f"{FAILURE_HEADER}The home URL lookup failed. Check animals's urls.py module. You're missing something in there.{FAILURE_FOOTER}")
    
    def test_response(self):
        """
        Does the response from the server contain the required string?
        """
        response = self.client.get(reverse('animals:home'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Requesting the home page failed. Check your URLs and view.{FAILURE_FOOTER}")
        self.assertContains(response, "Welcome to Animatch", msg_prefix=f"{FAILURE_HEADER}The home view does not return the expected response. Be careful you haven't missed any punctuation, and that your cAsEs are correct.{FAILURE_FOOTER}")
    
    def test_for_about_hyperlink(self):
        """
        Does the response contain the about hyperlink required in the exercise?
        Checks for both single and double quotes in the attribute. Both are acceptable.
        """
        response = self.client.get(reverse('animals:home'))
        
        single_quotes_check = '<a href=\'/animals/about/\'>About</a>' in response.content.decode() or '<a href=\'/animals/about\'>About</a>' in response.content.decode() 
        double_quotes_check = '<a href="/animals/about/">About</a>' in response.content.decode() or '<a href="/animals/about">About</a>' in response.content.decode()
        
        self.assertTrue(single_quotes_check or double_quotes_check, f"{FAILURE_HEADER}We couldn't find the hyperlink to the /animals/about/ URL in your home page. Check that it appears EXACTLY as in the book.{FAILURE_FOOTER}")


class AboutPageTests(TestCase):
    """
    Tests to check the about view.
    We check whether the view exists, the mapping is correct, and the response is correct.
    """
    def setUp(self):
        self.views_module = importlib.import_module('animals.views')
        self.views_module_listing = dir(self.views_module)
        self.project_base_dir = os.getcwd()
        self.template_dir = os.path.join(self.project_base_dir, 'templates', 'animals')
        self.about_response = self.client.get(reverse('animals:about'))
    
    
    def test_view_exists(self):
        """
        Does the about() view exist in animals's views.py module?
        """
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}We couldn't find the view for your about view! It should be called about().{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check you have defined your about() view correctly. We can't execute it.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        """
        Checks whether the about view has the correct URL mapping.
        """
        self.assertEquals(reverse('animals:about'), '/animals/about/', f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")
    
    def test_response(self):
        """
        Checks whether the view returns the required string to the client.
        """
        response = self.client.get(reverse('animals:about'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the about view, the server did not respond correctly. Is everything correct in your URL mappings and the view?{FAILURE_FOOTER}")
        self.assertContains(response, "animals says here is the about page.", msg_prefix=f"{FAILURE_HEADER}The about view did not respond with the expected message. Check that the message matches EXACTLY with what is requested of you in the book.{FAILURE_FOOTER}")
    
    def test_for_home_hyperlink(self):
        """
        Does the response contain the home hyperlink required in the exercise?
        Checks for both single and double quotes in the attribute. Both are acceptable.
        """
        response = self.client.get(reverse('animals:about'))
        
        single_quotes_check = '<a href=\'/animals/\'>home</a>' in response.content.decode()
        double_quotes_check = '<a href="/animals/">home</a>' in response.content.decode()
        
        self.assertTrue(single_quotes_check or double_quotes_check, f"{FAILURE_HEADER}We could not find a hyperlink back to the home page in your about view. Check your about.html template, and try again.{FAILURE_FOOTER}")

    def test_about_template_exists(self):
        """
        Tests the about template -- if it exists, and whether or not the about() view makes use of it.
        """
        template_exists = os.path.isfile(os.path.join(self.template_dir, 'about.html'))
        self.assertTrue(template_exists, f"{FAILURE_HEADER}The about.html template was not found in the expected location.{FAILURE_FOOTER}")
    
    def test_about_uses_template(self):
        """
        Checks whether the home view uses a template -- and the correct one!
        """
        self.assertTemplateUsed(self.about_response, 'animals/about.html', f"{FAILURE_HEADER}The about() view does not use the about.html template.{FAILURE_FOOTER}")
    
    def test_about_starts_with_doctype(self):
        """
        Is the <!DOCTYPE html> declaration on the first line of the about.html template?
        """
        self.assertTrue(self.about_response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your about.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
    
    def test_about_contains_required_text(self):
        """
        Checks to see whether the required text is on the rendered about page.
        """
        required = [
            "here is the about page.",
            "This tutorial has been put together by "
        ]
        
        for required_str in required:
            self.assertTrue(required_str in self.about_response.content.decode(), f"{FAILURE_HEADER}The expected string '{required_str}' was not found in the rendered /animals/about/ response.{FAILURE_FOOTER}")
    
    def test_about_contains_animals(self):
        """
        Checks whether the rendered about view has the picture of animals.
        """
        required_str = f"<img src=\"{settings.STATIC_URL}images/animals.jpg\" alt=\"Picture of animals\" />"
        self.assertTrue(required_str in self.about_response.content.decode(), f"{FAILURE_HEADER}The HTML markup to include the image of animals in the about template was not found. It needs to match exactly what we are looking for. Check the book.{FAILURE_FOOTER}")
    
class ModelTests(TestCase):
    """
    Are the models set up correctly, and do all the required attributes (post exercises) exist?
    """
    def setUp(self):
        category_py = Category.objects.get_or_create(name='Python', views=123, likes=55)
        Category.objects.get_or_create(name='Django', views=187, likes=90)
        
        Page.objects.get_or_create(category=category_py[0],
                                   title='Animatch',
                                   url='https://www.Animatch.com',
                                   views=156)
    
    def test_category_model(self):
        """
        Runs a series of tests on the Category model.
        Do the correct attributes exist?
        """
        category_py = Category.objects.get(name='Python')
        self.assertEqual(category_py.views, 123, f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(category_py.likes, 55, f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        
        category_dj = Category.objects.get(name='Django')
        self.assertEqual(category_dj.views, 187, f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(category_dj.likes, 90, f"{FAILURE_HEADER}Tests on the Category model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
    
    def test_page_model(self):
        """
        Runs some tests on the Page model.
        Do the correct attributes exist?
        """
        category_py = Category.objects.get(name='Python')
        page = Page.objects.get(title='Animatch')
        self.assertEqual(page.url, 'https://www.Animatch.com', f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.views, 156, f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.title, 'Animatch', f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.category, category_py, f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
    
    def test_str_method(self):
        """
        Tests to see if the correct __str__() method has been implemented for each model.
        """
        category_py = Category.objects.get(name='Python')
        page = Page.objects.get(title='Animatch')
        
        self.assertEqual(str(category_py), 'Python', f"{FAILURE_HEADER}The __str__() method in the Category class has not been implemented according to the specification given in the book.{FAILURE_FOOTER}")
        self.assertEqual(str(page), 'Animatch', f"{FAILURE_HEADER}The __str__() method in the Page class has not been implemented according to the specification given in the book.{FAILURE_FOOTER}")


    # Create your tests here.
