from django.urls import path
from . import views

urlpatterns = [
    path('showDigests', views.showDigests, name='showDigests'),
    path('digest/sendTest', views.sendTest, name='sendTest'),
    path('showDigest/<int:pk>', views.showDigest, name='showDigest')

]
