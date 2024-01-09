import environ
from django.db import transaction
from django.db.models import F
from rest_framework import views, status
from rest_framework.response import Response

from core_apps._config.exception_config.exception_handler import CustomException
from core_apps._config.payload_config.payload_validator import validate_payload
from core_apps.car_parts.models import Product
from core_apps.order.models import Cart, CartItem, Order, OrderItem
from core_apps.order.serializers import CartItemSerializer

env = environ.Env(
    DEBUG=(bool, False)
)


class CartView(views.APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.product_id = None
        self.session_id = None
        self.data = None

        self.request_data = None

    @transaction.atomic  # to rollback if any error occurs
    def post(self, request, ):

        try:
            self.request_data = request.data  # set request data
            self.validate_payload()  # define a function to validate payload
            self.retrieve_session()

            self.create_cart()  # define a function to save data

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

    def get(self, request):

        try:
            self.retrieve_session()  # define a function to retrieve session and set session id
            self.retrieve_cart()  # define a function to retrieve data
            self.retrieve_cart_items()

            return Response(self.data, status=status.HTTP_200_OK)  # return response

        except CustomException as error_message:
            error_response = {"message": "error: " + str(error_message)}  # define error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # return error response

        except Exception as ex:
            error_response = {"message": "error: " + str(ex)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id=None):
        try:
            self.product_id = product_id  # set product id
            self.retrieve_session()  # define a function to retrieve session and set session id
            self.retrieve_cart()  # define a function to retrieve data
            self.delete_product()  # define a function to delete data

            response = {"status": 200, "message": "Successfully Deleted"}
            return Response(response, status=status.HTTP_200_OK)  # return response

        except CustomException as error_message:
            error_response = {"message": "error: " + str(error_message)}  # define error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # return error response

        except Exception as ex:
            error_response = {"message": "error: " + str(ex)}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def validate_payload(self):
        is_valid, message = validate_payload(["product_id", "quantity"], self.request_data)  # validate payload

        if not is_valid:
            raise CustomException(message)  # raise exception if payload is not valid")

    def retrieve_cart(self):
        try:
            self.cart = Cart.objects.get(session_key=self.session_id)  # get Cart object
        except Cart.DoesNotExist:
            raise CustomException("Cart does not exist")  # raise exception if cart does not exist

    def retrieve_cart_items(self):
        cart_items = CartItem.objects.filter(cart_id=self.cart.id)
        serializer = CartItemSerializer(cart_items, many=True)
        self.data = serializer.data

    def create_cart(self):
        cart, created = Cart.objects.get_or_create(
            session_key=self.session_id
        )  # get or create Cart object

        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart.id,
            product_id=self.request_data['product_id'],
            defaults={'quantity': self.request_data['quantity']}
        )  # get or create CartItem object

        if not created:  # if cart item already exists
            cart_item.quantity = self.request_data['quantity']  # update quantity
            cart_item.save()  # save cart item

    def retrieve_session(self):
        session_key = self.request.session.session_key  # get session key
        if not session_key:  # if session key is None
            self.request.session.create()  # create session
            session_key = self.request.session.session_key  # get session key
        self.session_id = session_key  # set session id

    def delete_product(self):
        CartItem.objects.get(cart_id=self.cart.id, product_id=self.product_id).delete()  # delete cart item


class OrderView(views.APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_items = []
        self.cart = None
        self.session_id = None
        self.data = None

        self.request_data = None

    @transaction.atomic  # to rollback if any error occurs
    def post(self, request, ):

        try:
            self.request_data = request.data  # set request data
            self.validate_payload()  # define a function to validate payload
            self.retrieve_session()  # define a function to retrieve session and set session id
            self.retrieve_cart()  # define a function to retrieve data
            self.retrieve_cart_items()  # define a function to retrieve data
            self.create_order()  # define a function to create order

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

    def validate_payload(self):
        is_valid, message = validate_payload(
            ["customer_name", "customer_email", "customer_phone", "delivery_date", "delivery_time"],
            self.request_data)  # validate payload

        if not is_valid:
            raise CustomException(message)  # raise exception if payload is not valid")

    def retrieve_cart(self):
        try:
            self.cart = Cart.objects.get(session_key=self.session_id)  # get Cart object
        except Cart.DoesNotExist:
            raise CustomException("Cart does not exist")  # raise exception if cart does not exist

    def retrieve_cart_items(self):
        cart_items = CartItem.objects.filter(cart_id=self.cart.id)
        serializer = CartItemSerializer(cart_items, many=True)
        self.cart_items = serializer.data

    def create_order(self):
        order = Order.objects.create(
            customer_name=self.request_data['customer_name'],
            customer_email=self.request_data['customer_email'],
            customer_phone=self.request_data['customer_phone'],
            delivery_date=self.request_data['delivery_date'],
            delivery_time=self.request_data['delivery_time'],
        )

        total_price = 0.0
        for cart_item in self.cart_items:  # loop through cart items
            if not Product.objects.filter(id=cart_item['product_id'], quantity__gte=cart_item[
                "quantity"]).exists():  # check if product quantity is enough
                product_name = cart_item["product_name"]
                raise CustomException(f"{product_name} quantity is not enough")

            OrderItem.objects.create(
                order_id=order.id,
                product_id=cart_item['product_id'],
                quantity=cart_item['quantity']
            )  # create order item
            total_price = total_price + float(cart_item['total_price'])  # calculate total price

            Product.objects.filter(id=cart_item['product_id']).update(
                quantity=F('quantity') - cart_item['quantity']
            )  # update product quantity

        order.total_amount = total_price  # set total price
        order.save()  # save order

        self.cart.delete()  # delete cart

    def retrieve_session(self):
        session_key = self.request.session.session_key  # get session key
        if not session_key:  # if session key is None
            self.request.session.create()  # create session
            session_key = self.request.session.session_key  # get session key
        self.session_id = session_key  # set session id
