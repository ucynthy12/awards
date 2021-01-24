from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Rate,Project
from cloudinary.forms import CloudinaryFileField


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    profile_picture = CloudinaryFileField(
     options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 1000, 'height': 1000,
      'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
    })
    class Meta:

        model = Profile
        fields = [ 'profile_picture', 'bio']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
          'details': forms.Textarea(attrs={'rows':4, 'cols':30}),
        }
        fields = ('title','details','image', 'url')

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['design','usability','content','creativity']
        
