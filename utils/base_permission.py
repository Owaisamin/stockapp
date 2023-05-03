from django.http import JsonResponse
import random


def create_response(data, message, status_code):
    result = {
        "status_code": status_code,
        "message": message,
        "data": data
    }
    return JsonResponse(result)


def get_query_param(request, key, default):
    """
    @param request: request object
    @type request: request
    @param key: key to get data from
    @type key: str
    @param default: default variable to return if key is empty or doesn't exist
    @type default: str/None
    @return: key
    @rtype: str/None
    """
    if key in request.query_params:
        key = request.query_params.get(key)
        if key:
            return key
    return default


def generate_six_length_random_number():
    random_name = random.SystemRandom().randint(100000, 999999)
