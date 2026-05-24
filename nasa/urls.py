from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("earth/", views.earth, name="earth"),
    path("earth/eonet/", views.eonet, name="eonet"),
    path("gallery/", views.gallery, name="gallery"),
    path("gallery/download/", views.download_proxy, name="download_proxy"),
]