from django.urls import re_path
from tutorials import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path(r'^department$',views.ChatApi),
    re_path(r'^department/([0-9]+)$',views.ChatApi),

    # url(r'^employee$',views.employeeApi),
    # url(r'^employee/([0-9]+)$',views.employeeApi),

    #url(r'^employee/savefile',views.SaveFile)
]