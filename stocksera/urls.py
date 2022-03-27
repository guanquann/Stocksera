"""stocksera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

handler404 = 'app.views.custom_page_not_found_view'
handler500 = 'app.views.custom_error_view'
handler403 = 'app.views.custom_permission_denied_view'
handler400 = 'app.views.custom_bad_request_view'

urlpatterns = [
    path('', include('app.urls')),
    path('api/', include('api.urls')),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
]
