from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('account.urls')),
    path('blogs/', include('blog.urls')),
    path('doctors/', include('doctor.urls')),
]
