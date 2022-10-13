from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from app.forms import LoginForm, SignupForm


# Create your views here.

def home(request):
    return render(request, 'index.html', {
        'book_url': request.build_absolute_uri(reverse('get_book')),
        'is_guest': not request.user.is_authenticated
    })


@login_required
def user(request):
    return redirect('/')


@login_required
def get_book(request):
    pass


@login_required
def signout(request):
    logout(request)
    return redirect('/')


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user')

        errors = request.session.get('errors') or {}
        errors = errors.items()
        request.session['errors'] = None
        return render(request, 'login.html', {
            'errors': errors
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            clean_data = login_form.cleaned_data
            user = authenticate(
                username=clean_data.get('username'),
                password=clean_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('user')
            else:
                request.session['errors'] = {'username': ['Such user does not exist']}
                return redirect('login')
        else:
            request.session['errors'] = login_form.errors
            return redirect('login')


class Signup(View):
    def get(self, request):
        errors = request.session.get('errors') or {}
        errors = errors.items()
        request.session['errors'] = None
        return render(request, 'signup.html', {
            'errors': errors
        })

    def post(self, request):
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            clean_data = signup_form.cleaned_data
            user = User.objects.create_user(
                username=clean_data.get('username'),
                email=clean_data.get('email'),
                password=clean_data.get('password'),
            )
            return redirect('login')
        else:
            request.session['errors'] = signup_form.errors
            return redirect('signup')
