from django.urls import path

from authentication import views

urlpatterns = [
    # registration urls
    path('users/registration/', views.UserRegistrationView.as_view({'post': 'create'}), name='registration'),

    # login urls (use default from drf-simplejwt)
    path('login/token/', views.UserLoginView.as_view(), name='token_login'),
    path('login/token/refresh/', views.UserLoginRefreshView.as_view(), name='token_login_pairrefresh'),
]