from django.urls import path
from . import views

# take all the URL that will be used in this web application
urlpatterns = [
  path('', views.index, name='index')
]