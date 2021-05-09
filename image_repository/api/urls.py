from django.urls import path, include
from .views import AllAlbumsView, AlbumAddView, LoginView, LogoutView, UserView, RegistrationView, AlbumAddUsersView,AlbumUpdateView, UserImagesView, UserAlbumsView, ImageAllImagesView, ImageAddView, ImageUpdateView

urlpatterns = [
    path('images/', ImageAllImagesView.as_view()), 
    path('images/add', ImageAddView.as_view()),
    path('images/<pk>/edit', ImageUpdateView.as_view()),
    
    path('albums/', AllAlbumsView.as_view()),
    path('albums/add', AlbumAddView.as_view()),
    path('albums/<pk>/edit', AlbumUpdateView.as_view()),
    path('albums/<pk>/addusers', AlbumAddUsersView.as_view()),

    path('user/<user_pk>/images', UserImagesView.as_view()),
    path('user/<user_pk>/albums', UserAlbumsView.as_view()),
    
    path('auth/register', RegistrationView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/user', UserView.as_view()), 
    path('auth/logout', LogoutView.as_view())

]
