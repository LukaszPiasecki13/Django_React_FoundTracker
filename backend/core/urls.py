from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    # path('portfolio/', include('portfolio.urls')),
    path('api/', include('api.urls')),
]
