from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('contracts', views.ContractView, basename='contracts')
router.register('messages', views.MessageView, basename='messages')
router.register('commits', views.CommitView, basename='commits')

urlpatterns = [
    # path('contracts/', views.ContractCreateView.as_view(), name='contract_create'),
    # path('messages/', views.MessageCreateView.as_view({'post': 'create'}), name='message_create'),
    # path('commits/', views.CommitCreateView.as_view({'post': 'create'}), name='commit_create'),
    path('', include(router.urls)),
]