from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import datetime as dt
import random
from decimal import Decimal
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import ProfileSerializer, UserSerializer, ProjectSerializer
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            login(request, user)
            return redirect('login')
       
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def index(request):

    current_user = request.user
    date = dt.date.today()
    images = Project.all_images()
    random_image = random.choice(images)
    average = 0
    design=0
    usability=0
    creativity =0
    content =0
    ratings = Rate.objects.filter(post=random_image)
  

    if ratings:
        design = ratings.aggregate(Avg('design')).get('design__avg', 0.00)
        usability = ratings.aggregate(Avg('usability')).get('usability__avg', 0.00)
        creativity = ratings.aggregate(Avg('creativity')).get('creativity__avg', 0.00)
        content = ratings.aggregate(Avg('content')).get('content__avg', 0.00)
        average = round((design + usability + creativity+ content)/4,2)
      
    authenticated=False
    if request.user:
        authenticated = True
      
    
    return render(request,'index.html',{'images':images,'date':date,'current_user':current_user,'random_image':random_image,'design':design,'usability':usability,'creativity':creativity,'content':content,'average':average,'authenticated':authenticated,'ratings':ratings})



@login_required(login_url='login')
def projects(request,post_id):
    user = User.objects.get(username=request.user)
    post = Project.objects.get(pk= post_id)
    ratings = Rate.objects.filter(post=post)
    total_design = 0
    total_usability = 0
    total_creativity = 0
    total_content = 0
    total_average = 0
    rating_status = None
    a=  Rate.objects.filter(user=user)
    print(a)
    # if not ratings in  request.user.ratings.all():
    #     rating_status = False
    # else:
    #     rating_status = True

    if ratings:
      
        total_design = ratings.aggregate(Avg('design')).get('design__avg', 0.00)
    
        total_usability = ratings.aggregate(Avg('usability')).get('usability__avg', 0.00)
        total_creativity = ratings.aggregate(Avg('creativity')).get('creativity__avg', 0.00)
        total_content = ratings.aggregate(Avg('content')).get('content__avg', 0.00)
        average =(total_design + total_usability + total_creativity+ total_content)/4
        total_average =round(average,2) 
    
    boom = Project.objects.get(pk=post_id)
    current_user = request.user
    if request.method =='POST':

        rate_form = RateForm(request.POST)
        if rate_form.is_valid():          
            score=rate_form.save(commit=False)
            score_list=[int(request.POST.get('design')),int(request.POST.get('usability')),int(request.POST.get('creativity')),int(request.POST.get('content'))]
            
            average = sum(score_list)/len(score_list)
            score.average = average
            score.user = current_user
            score.post = boom
            score.save()

         
        return redirect('project',boom.id)
    else:
        rate_form = RateForm()
    context ={
        'total_design':total_design,
        'total_usability':total_usability,
        'total_creativity':total_creativity,
        'total_content':total_content,
        'total_average':total_average,
        'post':post,
        'rating_status':rating_status,
        'rate_form':rate_form,
    }
    return render(request,'projects.html',context)



def search_projects_title(request):
    if 'project_title' in request.GET and request.GET["project_title"]:
        results = request.GET.get("project_title")
        searched = Project.search_project(results)
        message = f"{results}"
      
        return render(request, "search.html",{'found':searched,'message':message})
    else:
        message = "You haven't searched for any project"
        return render(request, 'search.html',{"message":message})
   
     
@login_required(login_url='login')
def upload_form(request):
    current_user = request.user
    if request.method =='POST':
        project_form =ProjectForm(request.POST)
        if project_form.is_valid():          
            project=project_form.save(commit=False)
            project.user = current_user
            project.save()

            return redirect('index')
    else:
        project_form=ProjectForm()

    return render(request,'upload.html',{'project_form':project_form,})

@login_required(login_url='login')
def profile(request, username):

    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()
           
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    
    return render(request, 'profile.html',{'user_form': user_form, 'profile_form': profile_form,})



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer