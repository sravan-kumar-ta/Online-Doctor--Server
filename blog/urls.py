from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = router.urls

# (GET) api/posts/?page=<page-number> => get all post
# (POST) api/posts/ => create new post
# (GET) api/posts/11/ => get single post
# (DELETE) api/posts/11/ => delete a post
# (PUT) api/posts/11/ => update a post
# (PATCH) api/posts/11/ => update a specific field post1
# (GET) api/posts/get_my_posts/ => get request user's post1
# (POST) api/posts/25/like_or_dislike/ => like or dislike post
