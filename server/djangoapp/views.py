import logging
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


@csrf_exempt
def login_user(request):
    """
    Handle user login requests.

    Args:
        request: HTTP request object.

    Returns:
        JsonResponse: Response with authentication status and user information.
    """
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user:
        login(request, user)
        response_data["status"] = "Authenticated"
    return JsonResponse(response_data)


def logout_request(request):
    """
    Handle user logout requests.

    Args:
        request: HTTP request object.

    Returns:
        JsonResponse: Response confirming logout.
    """
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """
    Handle user registration requests.

    Args:
        request: HTTP request object.

    Returns:
        JsonResponse: Response with registration status and user information.
    """
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    try:
        User.objects.get(username=username)
        return JsonResponse(
            {
                "userName": username,
                "error": "Already Registered"
            })
    except User.DoesNotExist:
        logger.debug(f"{username} is a new user")
        user = User.objects.create_user(
            username=username, first_name=first_name,
            last_name=last_name, password=password, email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})


def get_cars(request):
    """
    Retrieve car makes and models.

    Args:
        request: HTTP request object.

    Returns:
        JsonResponse: Response with car models and their makes.
    """
    if not CarMake.objects.exists():
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        } for car_model in car_models]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """
    Retrieve dealerships, optionally filtered by state.

    Args:
        request: HTTP request object.
        state (str): State to filter dealerships by. Default is "All".

    Returns:
        JsonResponse: Response with dealership data.
    """
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """
    Retrieve reviews for a specific dealer.

    Args:
        request: HTTP request object.
        dealer_id (int): Dealer ID to fetch reviews for.

    Returns:
        JsonResponse: Response with dealer reviews.
    """
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment_response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = sentiment_response.get('sentiment')
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    """
    Retrieve details for a specific dealer.

    Args:
        request: HTTP request object.
        dealer_id (int): Dealer ID to fetch details for.

    Returns:
        JsonResponse: Response with dealer details.
    """
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    """
    Submit a review for a dealer.

    Args:
        request: HTTP request object.

    Returns:
        JsonResponse: Response indicating review submission status.
    """
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            logger.error(f"Error posting review: {err}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})
