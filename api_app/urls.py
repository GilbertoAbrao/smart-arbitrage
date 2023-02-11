from django.urls import path

from .views import ProfileAPIView
from .views import registration_view


app_name = "api_app"


urlpatterns = [

    # CRUD Profiles -----------------------------------------------------------------------
    path('profiles/', ProfileAPIView.as_view(), name='profiles_list'),    
    path('register/', registration_view, name='register'),    

    # path('suplier/', suplier_create_view, name='suplier_create'),
    # path('suplier/<uuid:pk>/', suplier_update_view, name='suplier_update'),
    # path('suplier/<uuid:pk>/delete/', suplier_delete_view, name='suplier_delete'),

]


