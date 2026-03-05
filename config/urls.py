from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from loans.views import apply_loan_view, my_loans_view, manager_review_view
from users.views import (
    home_view, register_view, login_view, logout_view, dashboard_view,
    user_list_view, user_create_view, user_edit_view, user_delete_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard_view),
    path('apply-loan/', apply_loan_view),
    path('my-loans/', my_loans_view),
    path('loans/review/<int:loan_id>/', manager_review_view),
    path('users/', user_list_view),
    path('users/create/', user_create_view),
    path('users/<int:user_id>/edit/', user_edit_view),
    path('users/<int:user_id>/delete/', user_delete_view),
    path('api/users/', include('users.urls')),
    path('api/loans/', include('loans.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
