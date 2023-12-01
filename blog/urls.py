from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = router.urls

# (GET) blog/posts/?page=<page-number> => get all post
# (POST) blog/posts/ => create new post
# (GET) blog/posts/11/ => get single post
# (DELETE) blog/posts/11/ => delete a post
# (PUT) blog/posts/11/ => update a post
# (PATCH) blog/posts/11/ => update a specific field post
# (GET) blog/posts/get_my_posts/ => get request user's post
# (POST) blog/posts/25/like_or_dislike/ => like or dislike post
