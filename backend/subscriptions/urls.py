from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from subscriptions import views

urlpatterns = [
    path('subscriptions/', views.SubscriptionsList.as_view(), name='subscriptions-list'),
    path('subscriptions/<int:pk>/', views.SubscriptionsDetail.as_view()),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)


