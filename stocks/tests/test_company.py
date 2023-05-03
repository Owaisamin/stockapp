from django.test import RequestFactory
from mixer.backend.django import mixer
import pytest
from stocks.stocks_controller import CompanyController


@pytest.fixture
def company_controller():
    return CompanyController()


@pytest.fixture
def api_rf():
    return RequestFactory()


def test_get_company(company_controller, api_rf):
    # Create some test data using mixer
    mixer.cycle(5).blend("stocks.Company", is_deleted=False)

    # Create a request object
    request = api_rf.get("/company")

    # Call the get_company method of the controller
    response = company_controller.get_company(request)

    # Assert that the response has a 200 status code
    assert response.status_code == 200

    # Assert that the response data is a dictionary
    assert isinstance(response.data, dict)

    # Assert that the response data has a count key
    assert "count" in response.data

    # Assert that the response data has a data key
    assert "data" in response.data


def test_create_company(company_controller, api_rf):
    # Create some test data
    data = {
        "company_name": "Test Company",
        "ticker": "TST",
        "industry": "Technology",
        "sector": "Information Technology",
        "address": "Cupertino, California, United States"

    }

    # Create a request object
    request = api_rf.post("/company", data=data)

    # Call the create_company method of the controller
    response = company_controller.create_company(request)

    # Assert that the response has a 200 status code
    assert response.status_code == 200

    # Assert that the response data is a dictionary
    assert isinstance(response.data, dict)

    # Assert that the response data has a ticker key
    assert "ticker" in response.data
    assert response.data["ticker"] == data["ticker"]


def test_update_company(company_controller, api_rf):
    # Create some test data using mixer
    company = mixer.blend("stocks.Company", is_deleted=False)

    # Create some updated test data
    updated_data = {
    "ticker": "AAPL",
    "address": "Cupertin1o, California, United States"
    }

    # Create a request object
    request = api_rf.patch(f"/company", data=updated_data)

    # Call the update_company method of the controller
    response = company_controller.update_company(request)

    # Assert that the response has a 200 status code
    assert response.status_code == 200

    # Assert that the response data is a dictionary
    assert isinstance(response.data, dict)

    # Assert that the response data has a ticker key
    assert "ticker" in response.data
    assert response.data["ticker"] == company.ticker

    # Refresh the company instance from the database
    company.refresh_from_db()

    # Assert that the company data has been updated
    assert company.company_name == updated_data["company_name"]
    assert company.address == updated_data["address"]


def test_delete_company(company_controller, api_rf):
    # Create some test data using mixer
    company = mixer.blend("stocks.Company", is_deleted=False)

    # Create a request object
    request = api_rf.delete(f"/company/?ticker={company.ticker}")

    # Call the delete_company method of the controller
    response = company_controller.delete_company(request)

    # Assert that the response has a 200 status code
    assert response.status_code == 200

    # Refresh the company instance from the database
    company.refresh_from_db()


