from django.urls import path

from app.views import home, user, get_book, logout_view, Login, Signup

urlpatterns = [
    path('', home),
    path('home/', home, name='home'),
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('logout/', logout_view, name='logout'),
    path('user/', user, name='user'),
    path('get-book/', get_book, name='get_book')
]
