from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as authviews
from subscriptions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', views.SubscriptionsList.as_view(), name='subscriptions-list'),
    path('subscriptions/<int:pk>/', views.SubscriptionsDetail.as_view()),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls'), name='api-auth'),
    path('account/register', views.UserCreate.as_view(), name='register'),
    path('', views.api_root),
    path('hooks/', views.hooks),
    path('payment/', views.payment),
    path('api-token-auth/', authviews.obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)


