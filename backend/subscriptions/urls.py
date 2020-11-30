from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from subscriptions import views

urlpatterns = [
    path('subscriptions/', views.SubscriptionsList.as_view()),
    path('subscriptions/<int:pk>/', views.SubscriptionsDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)


