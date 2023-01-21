from django.urls import path
from ads.views import AdListView, AdUserListView, AdView, CommentListView, CommentView

urlpatterns = [
    path("", AdListView.as_view()),
    path("me/", AdUserListView.as_view()),
    path("<int:pk>/", AdView.as_view()),
    path("<ad_pk>/comments/", CommentListView.as_view()),
    path("<str:ad_pk>/comments/<int:pk>/", CommentView.as_view())
]
