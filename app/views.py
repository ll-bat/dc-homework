import json
import os

from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
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


class CustomView(View):
    def get_error_tuples_from_request(self):
        errors = self.request.session.get('errors') or {}
        errors = errors.items()
        self.request.session['errors'] = None
        return errors

    def get_success_message_from_request(self):
        success_message = self.request.session.get('success_message', None)
        self.request.session['success_message'] = None
        return success_message

    def render(self, request, template_name, context=None, *args, **kwargs):
        if not context:
            context = {}

        if 'errors' not in context:
            context['errors'] = self.get_error_tuples_from_request()
        if 'success_message' not in context:
            context['success_message'] = self.get_success_message_from_request()

        return render(request, template_name, context, *args, **kwargs)


class Login(CustomView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))

        return self.render(request, 'auth/login.html')

    @staticmethod
    def post(request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            clean_data = login_form.cleaned_data
            user = authenticate(
                username=clean_data.get('username'),
                password=clean_data.get('password')
            )
            if user:
                login(request, user)
                return redirect(reverse('home'))
            else:
                request.session['errors'] = {'username': ['Such user does not exist']}
                return redirect('login')
        else:
            request.session['errors'] = login_form.errors
            return redirect('login')


class Signup(CustomView):
    def get(self, request):
        return self.render(request, 'auth/signup.html')

    @staticmethod
    def post(request):
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            clean_data = signup_form.cleaned_data
            User.objects.create_user(
                username=clean_data.get('username'),
                email=clean_data.get('email'),
                password=clean_data.get('password'),
            )
            request.session['success_message'] = 'You have signed up successfully'
            return redirect('login')
        else:
            request.session['errors'] = signup_form.errors
            return redirect('signup')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = kwargs.get("form")
        if not form:
            return context

        return {
            **context,
            "errors": form.errors.items()
        }


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"


class PasswordResetView(CustomView):
    def get(self, request):
        return self.render(request, 'auth/password_reset.html')

    @staticmethod
    def post(request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                user_uuid = urlsafe_base64_encode(force_bytes(user.pk))
                password_reset_link = reverse(
                    'password_reset_confirm',
                    kwargs={'uidb64': user_uuid, 'token': token}
                )
                return render(request, 'auth/password_reset.html', {
                    'password_reset_link': password_reset_link
                })
            else:
                request.session['errors'] = {
                    'email': ['No such email was found']
                }
                return redirect(reverse('password_reset'))
