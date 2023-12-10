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
    path('create_contract_docs/', views.CreateContractView.as_view(), name='create_contract_docs'),
    path('', include(router.urls)),
]