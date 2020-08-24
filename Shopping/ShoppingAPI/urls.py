from Shopping.ShoppingAPI.views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'ShoppingAPI'

urlpatterns = [
    path('<pk>/',product_detail_view,name="product_detail_view"),
    path('<pk>/update',product_update_view,name="update"),
    path('<pk>/delete',product_delete_view,name="delete"),
    path('create',product_create_view,name="create"),
    path('register',registration_view,name='register'),
    path('login',obtain_auth_token,name='login'),
    path('prdview',ApiProductView.as_view(),name='prdview'),
    path('billapi',ApiBillView.as_view(),name='billapi'),
    path('acc_properties',account_property_view,name='properties'),
    path('properties/update',update_account_view,name='update'),
    path('bill_detail_view/<pk>/',bill_detail_view,name='bill_detail_view'),
    path('UsrApiView',UsrApiView.as_view(),name='UsrApiView'),
    path('usrapi/<pk>/',usrapi,name='usrapi'),
]
