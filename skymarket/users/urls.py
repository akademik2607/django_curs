from django.urls import include, path
# from djoser.views import UserViewSet
# from rest_framework.routers import SimpleRouter
# TODO подключите UserViewSet из Djoser.views к нашим urls.py
# TODO для этокого рекоммендуется использовать SimpleRouter
from users.views import UserListView, UserMeView, ChangePasswordView, UserRetrieveView

urlpatterns = [
    path("", UserListView.as_view()),
    path("me/", UserMeView.as_view()),
    path("set_password/", ChangePasswordView.as_view()),
    path("<int:pk>/", UserRetrieveView.as_view())
]
