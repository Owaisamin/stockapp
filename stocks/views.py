from rest_framework import viewsets
from stocks.stocks_controller import *
from utils.base_authentication import JWTAuthentication
from stocks.serializers import LoginSerializer

login_controller = LoginController()
company_controller = CompanyController()
stock_price_controller = StockPriceController()
fetch_data_controller = FetchDataController()


# Create your views here.
class LoginAPIView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer

    def post(self, request):
        return login_controller.login(request)
    
class CompanyView(viewsets.ModelViewSet):
    """
    Endpoints for Region CRUDs.
    """
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        return company_controller.get_company(request)

    def create(self, request):
        return company_controller.create_company(request)

    def update(self, request):
        return company_controller.update_company(request)

    def destroy(self, request):
        return company_controller.delete_company(request)
    

class StockPriceView(viewsets.ModelViewSet):
    """
    Endpoints for Region CRUDs.
    """
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        return stock_price_controller.get_stock_price(request)

    def create(self, request):
        return stock_price_controller.create_stock_price(request)

class FetchDataView(viewsets.ModelViewSet):
    """
    Endpoints for Region CRUDs.
    """
    authentication_classes = (JWTAuthentication,)

    def create(self, request):
        return fetch_data_controller.create(request)

