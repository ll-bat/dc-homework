import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from app.forms import LoginForm, SignupForm
from app.helpers import validate_isbn
from app.models import Book
from app.services import GoogleBookApiService


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
    isbn = request.GET.get('isbn', '')
    if not validate_isbn(isbn):
        error = json.dumps({'non_field_errors': ['Please, provide valid ISBN']})
        return HttpResponse(content=error, status=400)

    book = Book.objects.filter(isbn=isbn).first()
    if book:
        json_data = json.dumps([model_to_dict(book)])
        return HttpResponse(json_data)
    else:
        result = GoogleBookApiService.get_book_by_isbn(isbn)
        if not result['ok']:
            error = json.dumps({'non_field_errors': [result['error_message']]})
            return HttpResponse(content=error, status=400)

        api_data = result['data']
        if not api_data:
            # no book was found
            return HttpResponse(json.dumps([]))

        api_field_to_model_field_mapper = {
            'title': 'title',
            'description': 'description',
            'authors': 'authors',
            'publisher': 'publisher',
            'publishedDate': 'published_date',
            'pageCount': 'page_count',
            'categories': 'categories',
            'imageLinks': 'image_links',
            'language': 'language',
            'previewLink': 'preview_link',
            'infoLink': 'info_link',
        }

        model_data = {
            model_key: api_data.get(api_key)
            for api_key, model_key in api_field_to_model_field_mapper.items()
        }

        new_book = Book(**{
            **model_data,
            'isbn': isbn,
            'created_by': request.user,
            'updated_by': request.user,
        })
        try:
            new_book.save()
        except Exception as e:
            pass

        json_data = json.dumps([model_to_dict(new_book)])
        return HttpResponse(json_data)


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
