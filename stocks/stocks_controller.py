from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
import yfinance as yf
from utils.reusable_methods import *
from utils.response_messages import *
from rest_framework.pagination import LimitOffsetPagination
from stocks_project.settings import *
from stocks.models import *
from stocks.serializers import *
from django.contrib.auth import authenticate
from datetime import datetime




# Create your views here.
class LoginController:
    """
    An endpoint for Login.
    """
    serializer_class = LoginSerializer

    def login(self, request):
        request.POST._mutable = True
        request.data["email"] = request.data.get("email").strip()
        request.data["password"] = request.data.get("password").strip()
        request.POST._mutable = True
        email = request.data.get("email")
        password = request.data.get("password")
        serialized_data = self.serializer_class(data=request.data)
        if not serialized_data.is_valid():
            return create_response({}, message=serialized_data.errors, status_code=401)
        user = authenticate(email=email, password=password)
        if not user:
            return create_response({}, message=INCORRECT_EMAIL_OR_PASSWORD, status_code=401)
        response_data = {
            "token": user.get_access_token()
        }
        Token.objects.update_or_create(defaults={"user": user, "token": response_data.get("token")}, user_id=user.guid)
        return create_response(response_data, SUCCESSFUL, status_code=200)
    
class CompanyController:
    serializer_class = CompanySerializer

    def get_company(self, request):
        kwargs = {}
        limit = get_query_param(request, 'limit', None)
        offset = get_query_param(request, 'offset', None)

        kwargs["is_deleted"] = False
        data = self.serializer_class.Meta.model.objects.filter(**kwargs)
        count = data.count()
        if limit and offset:
            pagination = LimitOffsetPagination()
            data = pagination.paginate_queryset(data, request)

        serialized_data = self.serializer_class(data, many=True).data
        response_data = {
            "count": count,
            "data": serialized_data
        }
        return create_response(response_data, SUCCESSFUL, status_code=200)

    def create_company(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            response_data = serialized_data.save()
            return create_response(self.serializer_class(response_data).data, SUCCESSFUL, status_code=200)
        return create_response({}, UNSUCCESSFUL, status_code=500)

    def update_company(self, request):
        if "ticker" not in request.data:
            return create_response({}, TICKER_NOT_PROVIDED, 404)
        else:
            instance = self.serializer_class.Meta.model.objects.filter(ticker=request.data.get("ticker"), is_deleted=False).first()
            if not instance:
                return create_response({}, NOT_FOUND, 400)
            serialized_data = self.serializer_class(instance, data=request.data, partial=True)
            if serialized_data.is_valid():
                response_data = serialized_data.save()
                return create_response(self.serializer_class(response_data).data, SUCCESSFUL, 200)
            return create_response({}, UNSUCCESSFUL, status_code=500)

    def delete_company(self, request):
        if "ticker" not in request.query_params:
            return create_response({}, TICKER_NOT_PROVIDED, 404)
        instance = self.serializer_class.Meta.model.objects.filter(ticker=request.query_params.get("ticker"),
                                                                   is_deleted=False).first()
        if not instance:
            return create_response({}, NOT_FOUND, 400)
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        return create_response({}, SUCCESSFUL, 200)
    
class StockPriceController:
    serializer_class = StockPriceSerializer

    def get_stock_price(self, request):
        kwargs = {}
        ticker = get_query_param(request, "ticker", None)
        start_date = get_query_param(request, "start_date", None)
        end_date = get_query_param(request, "end_date", None)
        id = get_query_param(request, "id", None)
        limit = get_query_param(request, 'limit', None)
        offset = get_query_param(request, 'offset', None)

        if id:
            kwargs["id"] = id

        if ticker:
            kwargs["company"] = ticker

        if start_date:
            kwargs["date__gte"] = start_date

        if end_date:
            kwargs["date__lte"] = end_date
        

        kwargs["is_deleted"] = False
        data = self.serializer_class.Meta.model.objects.filter(**kwargs)
        count = data.count()
        if limit and offset:
            pagination = LimitOffsetPagination()
            data = pagination.paginate_queryset(data, request)

        serialized_data = self.serializer_class(data, many=True).data
        response_data = {
            "count": count,
            "data": serialized_data
        }
        return create_response(response_data, SUCCESSFUL, status_code=200)

    def create_stock_price(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            response_data = serialized_data.save()
            return create_response(self.serializer_class(response_data).data, SUCCESSFUL, status_code=200)
        return create_response({}, UNSUCCESSFUL, status_code=500)
    

class FetchDataController:
    queryset = StockPrice.objects.all()

    def create(self, request, *args, **kwargs):
        ticker = request.data.get('ticker')
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()

        company = get_object_or_404(Company, ticker=ticker)
        data = yf.download(ticker, start=start_date, end=end_date)
        for index, row in data.iterrows():
            stock_price = StockPrice(
                company=company,
                date=index,
                open=row['Open'],
                close=row['Close'],
                volume=row['Volume'],
            )
            stock_price.save()

        return Response({'message': 'Stock price data saved successfully.'})

        
        

    