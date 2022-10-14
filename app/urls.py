from django.urls import path

from app.views import home, get_book, logout_view, Login, Signup, PasswordResetCompleteView, PasswordResetDoneView,\
    PasswordResetConfirmView, PasswordResetView

urlpatterns = [
    path('', home),
    path('home/', home, name='home'),

    path('get-book/', get_book, name='get_book'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', Signup.as_view(), name='signup'),

    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("password_reset", PasswordResetView.as_view(), name="password_reset")
    # path('accounts/', include('django.contrib.auth.urls')),
]
