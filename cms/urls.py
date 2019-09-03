"""CMS urls."""
from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [

    path(
        '',
        views.ImageCreate.as_view(),
        name='home'
    ),
    path(
    	'<int:image_id>/',
    	views.ImageDetailView.as_view(),
    	name='image-detail'
    ),

]
