from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('dashboard', views.dashboardView, name='dashboard_page'),
    path('', views.loginUser, name="login"),
    path('register', views.userRegister, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('create_task/', views.createTask, name="create_task"),
    path('view_task_description/<int:task_id>/', views.viewTaskDescription, name="view_task_description"),
    path('update_task/<int:task_id>/', views.updateTask, name="update_task"),
    path('mark_task_completed/<int:task_id>/', views.markTaskCompleted, name='mark_task_completed'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),    
]
