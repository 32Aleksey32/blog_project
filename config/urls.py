from django.contrib import admin
from django.urls import include, path

from blog.views import Signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', Signup.as_view(), name='signup'),
]
