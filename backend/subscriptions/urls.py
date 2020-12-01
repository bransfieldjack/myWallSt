from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as authviews
from subscriptions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', views.SubscriptionsList.as_view(), name='subscriptions-list'),
    path('subscriptions/<int:pk>/', views.SubscriptionsDetail.as_view(), name='subscription'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='single-user'),
    path('api-auth/', include('rest_framework.urls'), name='api-auth'),
    path('account/register', views.UserCreate.as_view(), name='register'),
    path('', views.api_root),
    path('hooks/', views.hooks),
    path('payment/', views.payment),
    path('api-token-auth/', authviews.obtain_auth_token)    # Built-in drf view for retrieval of tokens for existing users.
]

urlpatterns = format_suffix_patterns(urlpatterns)


