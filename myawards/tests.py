from django.test import TestCase
from .models import *

# Create your tests here.

class ProfileTestClass(TestCase):
    def setUp(self):
        self.user = User(id=1,username='ucynthy',password='zion')
        self.user.save()
    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
    
    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()
    
class ProjectTestClass(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1,username='ucynthy')

        self.project = Project.objects.create(id=1,user= self.user,title='my first project',details='this is a test description',url='https://res.cloudinary.com/ucynthy12/image/upload/v1607257084/493d6f4f3ffa33eabaa6e539e8cb6293_ioree4-removebg-preview_fzqok5.png',published='December-21-2020')

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_save_project(self):
        self.project.save_project()
        project = Project.objects.all()
        self.assertTrue(len(project) > 0)

    def test_get_projects(self):
        self.project.save()
        project = Project.all_images()
        self.assertTrue(len(project) > 0)

    def test_search_project(self):
        self.project.save_project()
        find_project = Project.search_project('my first project')
        self.assertTrue(len(find_project) >= 1)

    def test_delete_project(self):
        self.project.save_project()
        self.project.delete_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects) == 0)


class RateTestClass(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1,username='ucynthy')

        self.project = Project.objects.create(id=1,user= self.user,title='my first project',details='this is a test description',url='https://res.cloudinary.com/ucynthy12/image/upload/v1607257084/493d6f4f3ffa33eabaa6e539e8cb6293_ioree4-removebg-preview_fzqok5.png',published='December-21-2020')

        self.rating = Rate.objects.create(id=1, design=6, usability=7, creativity=9, content=9, user=self.user, post=self.project)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rate))

    def test_save_rating(self):
        self.rating.save_rate()
        rating = Rate.objects.all()
        self.assertTrue(len(rating) > 0)

   