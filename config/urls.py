from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from loans.views import (
    apply_loan_view,
    my_loans_view,
)

from users.views import (
    home_view,
    register_view,
    login_view,
    logout_view,
    dashboard_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web pages
    path('', home_view),
    path('register/', register_view),   
    path('login/', login_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard_view),
    path('apply-loan/', apply_loan_view),
    path('my-loans/', my_loans_view),


    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/loans/', include('loans.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
