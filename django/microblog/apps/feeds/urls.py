from django.urls import path

from feeds.api.views import FeedView, CreatePostView

app_name = 'feeds'

urlpatterns = [
    path('', FeedView.as_view(), name='list'),
    path('<int:user_id>/', FeedView.as_view(), name='list'),
    path('<int:user_id>/posts/', CreatePostView.as_view(), name="create_post")
]