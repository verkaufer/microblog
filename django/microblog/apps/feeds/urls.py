from django.urls import path

from feeds.api.views import CurrentUserFeedView, SpecificUserFeedView, CreatePostView

app_name = 'feeds'

urlpatterns = [
    path('', CurrentUserFeedView.as_view(), name='list_feeds'),
    path('<int:user_id>/', SpecificUserFeedView.as_view(), name='feed_detail'),
    path('posts/', CreatePostView.as_view(), name="create_post")
]