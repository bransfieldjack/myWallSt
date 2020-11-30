from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from subscriptions import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', views.SubscriptionsList.as_view(), name='subscriptions-list'),
    path('subscriptions/<int:pk>/', views.SubscriptionsDetail.as_view()),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('account/register', views.UserCreate.as_view(), name='register'),
    path('', views.api_root),
    path('hooks/', views.hooks),

    path('payment/', views.payment),
]

urlpatterns = format_suffix_patterns(urlpatterns)


