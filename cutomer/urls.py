from django.urls import path
from.views import *


urlpatterns = [
    path('reg',RegView.as_view(),name="reg"),
    path('h',CustHome.as_view(),name="home"),
    path('pro',ProductView.as_view(),name="product"),
    path('fdet/<int:pid>',Furnituredetailview.as_view(),name="fdet"),
    path('acart/<int:pid>',addcart,name="acart"),
    path('vcart',Cartview.as_view(),name="vcart"),
    path('delcart/<int:id>',deletecartitem,name="delcart"),
    path('checkout/<int:cid>',Checkoutview.as_view(),name="checkout"),
    path('order',Myorder.as_view(),name="myorder"),
    path('cancelorder/<int:id>',cancel_order,name="cancelorder"),
    path('lgout',Logoutview.as_view(),name="lgout"),
    path('search',Search.as_view(),name="search"),
    
    
    
]
