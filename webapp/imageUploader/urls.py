from django.conf.urls import url

from . import views

urlpatterns = [
    # Regex match to decide which view should be called for specific url
    url(r'uploadImage/$', views.uploadImage, name='uploadImage'),
    url(r'deleteImage/$', views.deleteImage, name='deleteImage'),
    url(r'editImage/$', views.editImage, name='editImage'),
]