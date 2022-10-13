from django.urls import path

from app.views import home, user, get_book, signout, Login, Signup

urlpatterns = [
    path('', home),
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('signout/', signout, name='signout'),
    path('user/', user, name='user'),
    path('get-book/', get_book, name='get_book')
]
