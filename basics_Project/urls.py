"""
URL configuration for basics_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from basics_Project import settings
from main_app import views

urlpatterns = ([
    path('', views.home_page, name = "home"),
    path('about', views.about, name = "about"),
    path('donate', views.donate, name = "donate"),
    path('contact', views.contact, name = "contact"),
    path('team', views.team, name = "team"),
    path('employees', views.employee, name = "all"),
    path('signin', views.signin, name = "signin"),
    path('signout', views.signout, name = "signout"),
    path('search', views.search_employees, name = "search"),

    path('employees/<int:emp_id>', views.employee_details, name = "details"),
    path('employees/delete/<int:emp_id>', views.employee_delete, name = "delete"),
    path('employees/update/<int:emp_id>', views.employee_update, name = "update"),


    # path('data', views.data),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT))
# "employees/<int:emp_id>"
# python manage.py migrate
# python manage.py createsuperuser

