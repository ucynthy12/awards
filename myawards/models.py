from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
import datetime as dt

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture = CloudinaryField('image')
    bio = models.TextField(default="My Bio", blank=True)
    name = models.CharField(max_length=120,blank=True)
    projects = models.ForeignKey('Project',on_delete= models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name
    
    def save_profile(self):
        self.save()
    
    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls):
        return Profile.objects.all()
    
    class Meta:
        db_table = 'profiles'

    
class Project(models.Model):
    title = models.CharField(max_length= 150)
    details = models.TextField()
    url = models.URLField(max_length=500)
    user = models.ForeignKey(User,on_delete =models.CASCADE,null=True)
    image = CloudinaryField('image')
    vote = models.IntegerField(default=0)
    published = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.title
    
    def save_project(self):
        self.save()
    
    @classmethod
    def all_images(cls):
        images = Project.objects.all()
        print(images)
        return images
    
    @classmethod
    def one_image(cls,project):
        project = cls.objects.get(id = project)
        return project

    @classmethod
    def search_project(cls,search_term):
        results = cls.objects.filter(title__icontains=search_term)
        return results

    def delete_project(self):
        self.delete()
    
    class Meta:

        db_table = 'projects'
        ordering = ['-id']

class Rate(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE,related_name='jugde')
    post = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='ratings', null=True)
    design = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)], null=True)
    usability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)], null=True)
    creativity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)], null=True)
    content = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)], null=True)
    average = models.IntegerField(default=0)

    def save_rate(self):
        self.save()
    
    def delete_rate(self):
        self.delete()
    
    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings
    def __str__(self):

        return f'{self.post} Rating'
    class Meta:

        db_table = 'ratings'