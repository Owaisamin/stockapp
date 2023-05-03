from django.urls import path
from stocks.views import *

urlpatterns = [
    
    path('company', CompanyView.as_view(
        {
            "get": "get",
            "post": "create",
            "patch": "update",
            "delete": "destroy"
        }
    )
         ),

    path('stockprice', StockPriceView.as_view(
        {
            "get": "get",
            "post": "create",
        }
    )
         ),
    path('fetchdata', FetchDataView.as_view(
        {
            "post": "create",
        }
    )
         ),

    path('login', LoginAPIView.as_view({"post": "post"})),
    ]
