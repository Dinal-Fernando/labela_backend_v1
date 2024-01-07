from datetime import datetime

import environ
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import views, status
from rest_framework.response import Response

from core_apps._config.exception_config.exception_handler import CustomException
from core_apps._config.payload_config.payload_validator import validate_payload
from core_apps.car_parts.models import Product
from core_apps.car_parts.serializers import ProductSerializer

env = environ.Env(
    DEBUG=(bool, False)
)


class ProductView(views.APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._product_id = None
        self.products = None
        self.product = None
        self.count = 0
        self.data = None
        self.keyword = None
        self.page_number = None
        self.limit = None

        self.request_data = None

    @transaction.atomic  # to rollback if any error occurs
    def post(self, request, ):

        try:
            self.request_data = request.data  # set request data
            self.validate_payload()  # define a function to validate payload
            self.save_data()  # define a function to save data

            response = {"status": 200, "message": "Successfully created"}  # define response
            return Response(response, status=status.HTTP_201_CREATED)  # return response

        except CustomException as error_message:
            transaction.set_rollback(True)  # rollback if any error occurs
            error_response = {"status": 490, "message": "error: " + str(error_message)}  # define error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # return error response

        except Exception as ex:
            transaction.set_rollback(True)
            error_response = {"message": "error: " + str(ex)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic  # to rollback if any error occurs
    def put(self, request, product_id=None):

        try:
            self.request_data = request.data  # set request data
            self.product_id = product_id  # set product id
            self.update_data()  # define a function to update data

            response = {"status": 200, "message": "Successfully updated"}
            return Response(response, status=status.HTTP_201_CREATED)  # return response

        except CustomException as error_message:
            transaction.set_rollback(True)  # rollback if any error occurs
            error_response = {"message": "error: " + str(error_message)}  # define error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # return error response

        except Exception as ex:
            transaction.set_rollback(True)
            error_response = {"message": "error: " + str(ex)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id=None):
        try:
            self.product_id = product_id  # set product id
            self.delete_data()  # define a function to delete data

            response = {"status": 200, "message": "Successfully Deleted"}
            return Response(response, status=status.HTTP_201_CREATED)  # return response

        except CustomException as error_message:
            error_response = {"message": "error: " + str(error_message)}  # define error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # return error response

        except Exception as ex:
            error_response = {"message": "error: " + str(ex)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, product_id=None):

        try:
            self.product_id = product_id  # set product id
            self.populate_variables()  # define a function to populate variables

            if self.product_id:
                self.get_details()
            else:
                self.get_list()

            return Response(self.data, status=status.HTTP_201_CREATED)  # return response

        except CustomException as error_message:
            error_response = {"message": "error: " + str(error_message)}  # define error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # return error response

        except Exception as ex:
            error_response = {"message": "error: " + str(ex)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def validate_payload(self):
        is_valid, message = validate_payload(["name", "description", "price", "quantity"], self.request_data)

        if not is_valid:
            raise CustomException(message)  # raise exception if payload is not valid")

    @property
    def product_id(self):
        return self._product_id  # return product id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value  # set product id
        if self._product_id:  # if product id is not None
            self.retrieve_product()  # define a function to retrieve product

    def retrieve_product(self):
        try:
            self.product = Product.objects.get(id=self.product_id, is_delete=False)  # get product
        except Product.DoesNotExist:
            raise CustomException("Product does not exist")  # raise exception if product does not exist

    def retrieve_products(self):
        self.products = Product.objects.filter(is_delete=False).order_by("-id")  # get products

    def save_data(self):
        if Product.objects.filter(name=self.request_data["name"], is_delete=False).exists():
            raise CustomException("Product name already exist")  # raise exception if product already exist

        self.product = Product.objects.create(
            name=self.request_data["name"],
            description=self.request_data["description"],
            price=self.request_data["price"],
            quantity=self.request_data["quantity"],
            created_on=datetime.now()
        )  # create product

    def update_data(self):
        if "name" in self.request_data:
            if Product.objects.filter(name=self.request_data["name"],
                                      is_delete=False).exists():  # check if product name already exist
                raise CustomException("Product name already exist")  # raise exception if product already exist

            self.product.name = self.request_data["name"]  # set product name

        if "description" in self.request_data:  # check if description is in request data
            self.product.description = self.request_data["description"]  # set product description

        if "price" in self.request_data:  # check if price is in request data
            self.product.price = self.request_data["price"]  # set product price

        if "quantity" in self.request_data:  # check if quantity is in request data
            self.product.quantity = self.request_data["quantity"]  # set product quantity

        self.product.updated_on = datetime.now()  # set updated on
        self.product.save()  # save updated product

    def delete_data(self):
        self.product.is_delete = True  # set is delete to true
        self.product.save()

    def populate_variables(self):
        self.limit = int(self.request.GET.get('limit')) if self.request.GET.get('limit') else None  # set limit
        self.page_number = int(self.request.GET.get('page')) if self.request.GET.get(
            'page') else None  # set page number
        self.keyword = self.request.GET.get('keyword') if self.request.GET.get('keyword') else None  # set keyword

    def get_details(self):
        serializer = ProductSerializer(self.product, many=False)  # serialize product
        self.data = serializer.data  # set data

    def handle_pagination(self):
        paginator = Paginator(self.products, self.limit)  # set paginator
        if self.page_number not in list(paginator.page_range):  # check if page number is in paginator page range
            raise CustomException("Invalid page number")  # raise exception if page number is invalid

        self.products = paginator.page(self.page_number)  # set products

    def get_list(self):
        self.retrieve_products()  # define a function to retrieve products
        if self.keyword:  # if keyword is not None
            self.products = self.products.filter(name__icontains=self.keyword)  # filter products by keyword

        self.count = self.products.count()  # set count
        if self.page_number and self.limit:  # if page number and limit is not None
            self.handle_pagination()  # define a function to handle pagination

        serializer = ProductSerializer(self.products, many=True)  # serialize products
        self.data = serializer.data  # set data
