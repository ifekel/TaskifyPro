from django.urls import path, include
from .views import UserViewset, AuthViewset, TaskViewset, AuthStatusView
from rest_framework.routers import SimpleRouter

userRouter = SimpleRouter()
userRouter.register('user', UserViewset, basename='user')

authRouter = SimpleRouter()
authRouter.register('auth', AuthViewset, basename='auth')

taskRouter = SimpleRouter()
taskRouter.register('task', TaskViewset, basename='task')

urlpatterns = [
    path('', include(userRouter.urls)),
    path('', include(authRouter.urls)),
    path('', include(taskRouter.urls)),
    path('auth/status/', AuthStatusView.as_view(), name='auth-status')
]