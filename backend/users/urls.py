from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register(r'', views.UserView, basename='user')

urlpatterns = [
    path(
        'profile/',
        views.UserPrivateDataView.as_view(
            {'delete': 'destroy', 'patch': 'partial_update', 'put': 'update', 'get': 'retrieve'}
        ),
        name='user_profile'
    ),
    path('', include(router.urls))
]