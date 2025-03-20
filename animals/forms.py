from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from animals.models import UserProfile, Animal

class AnimalForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the animal's name.")
    about = forms.CharField(widget=forms.Textarea, help_text="Please provide information about the animal.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Animal
        fields = ('name', 'species', 'breed', 'age', 'sex', 'about', 'picture', 'sociable')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')