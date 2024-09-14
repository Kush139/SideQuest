from django.urls import path
from .views import (
    SignupView, SigninView, LogoutView, ProfileDetailView,
    PostListCreateView, LikePostView, FollowView, SearchView,
    IndexView, SettingsView, TermsView, UserProfileView, GenerateTaskView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('posts/', PostListCreateView.as_view(), name='posts'),
    path('like/', LikePostView.as_view(), name='like-post'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('search/', SearchView.as_view(), name='search'),
    path('index/', IndexView.as_view(), name='index'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('user/<str:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('generate-task/', GenerateTaskView.as_view(), name='generate-task')
]
