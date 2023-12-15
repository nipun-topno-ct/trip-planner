"""
URL configuration for trip_planner project.

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
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from places.views import GetPlacesView
from places.views import GetHotspotsView
from trips.views import plan_trip
from expense.views import expense
from expense.views import get_expenses
from expense.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/fetch-places', GetPlacesView.as_view()),
    re_path('api/plan-trip', plan_trip, name='plan_trip'),
    re_path('api/fetch-hotspot', GetHotspotsView.as_view()),
    re_path('api/expense/add',expense,name='expense'),
    re_path('api/expenses/total', get_expenses, name='get_all_expenses'),
    re_path('api/expense/delete/<int:expense_id>', delete_expense, name='delete_expense'),
    re_path(r'^api/get_tip/(?P<text>.*)/$', get_tip, name='get_tip')
]
