
from django.contrib import admin
from django.urls import path,include
from authorization.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authorization.urls"))
    
]
