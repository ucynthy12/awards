from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)
router.register('profile', views.ProfileViewSet)

urlpatterns = [
    path('account/',include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('accounts/register/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), {"next_page": '/'}),
    path('project/<post_id>',views.projects, name='project'),
    path('search/', views.search_projects_title, name='search'),
    path('uploads/',views.upload_form,name='uploads'),
    path('profile/<username>/', views.profile, name='profile'),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token)

]