import json
from rest_framework import viewsets ,permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from bookstore.models import Book ,Author ,Category ,Cart ,CartItem, Order, OrderItem
from bookstore.serializers import (BookSerializer ,AuthorSerializer ,CategorySerializer ,AuthorSerializerResponse,
                                   BookSerializerResponse,CartSerializer,CartSerializerResponse ,OrderItemSerializer,
                                   OrderSerializer)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = BookSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({"msg": "Book added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=400)
        except Exception as ex:
            print("ex", ex)
            return Response({"msg": "Something went wrong!"}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            # Use get_object() to retrieve the instance based on the URL parameter (pk/id)
            instance = self.get_object()
            if instance:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"msg": "Book updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        except Book.DoesNotExist:
            return Response({"msg": "Book does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"msg": "Something went wrong!", "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = BookSerializerResponse(queryset, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"msg": "Something went wrong!","data":[], "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        try:
            serializer = AuthorSerializer(data=request.data ,context = {'user':request.user})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({"msg": "Author created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=400)
        except Exception as ex:
            print("ex",ex)
            return Response({"msg":"Something went wrong!"},status=400)


    def update(self, request, *args, **kwargs):
        try:
            # Use get_object() to retrieve the instance based on the URL parameter (pk/id)
            instance = self.get_object()
            if instance.created_by == request.user:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"msg": "Author updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        except Author.DoesNotExist:
            return Response({"msg": "Author does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"msg": "Something went wrong!", "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = AuthorSerializerResponse(queryset, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"msg": "Something went wrong!", "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data ,context = {'user':request.user})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response({"msg": "Category created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            print("in here e",e)
            return Response({"msg": "Something went wrong"}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            # Use get_object() to retrieve the instance based on the URL parameter (pk/id)
            instance = self.get_object()
            if instance.created_by == request.user:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"msg": "Category updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "You are not allowed to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        except Category.DoesNotExist:
            return Response({"msg": "Author does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"msg": "Something went wrong!", "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        # Check if the user already has a cart
        existing_cart = Cart.objects.filter(user=user).first()
        if existing_cart:
            # If user already has a cart, you may choose to update or return an error
            return Response({"detail": "User already has a cart."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating a new cart
        serializer = self.get_serializer(data=request.data,context={'user': request.user,'items':json.loads(request.data.get('items',[]))})
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"msg":"Card created successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        try:
            try:
                instance = Cart.objects.get(user=request.user)
                serializer = self.get_serializer(instance, data=request.data, partial=True, context={'user': request.user,'items':json.loads(request.data.get('items',[]))})
                if serializer.is_valid(raise_exception=False):
                    serializer.save()
                    return Response({'msg':"Cart updated successfully"},status=200)
                else:
                    return Response(serializer.errors)
            except:
                return Response({"msg": "Cart does not exists"}, status=400)

        except Exception as ex:
            print("ex",ex)
            return Response({"msg":"Something went wrong"},status=400)

    @action(detail=True, methods=['delete'])
    def delete_cart(self, request, *args, **kwargs):
        try:
            whole_cart = request.query_params.get('whole_cart', None)
            books_list = request.query_params.get('books_list', None)
            books_list = json.loads(books_list)
            try:
                instance = Cart.objects.get(user=request.user)
            except:
                instance = None
            # Check if the cart belongs to the current user (optional, depending on your logic)
            if instance.user != request.user:
                return Response({"detail": "You do not have permission to delete this cart."},
                                status=status.HTTP_403_FORBIDDEN)
            if whole_cart is None:
                all_cart = Cart.objects.filter(user=request.user)
                all_cart.delete()
                return Response({"msg": "Cart deleted successfully"}, status=200)
            if len(books_list) > 0:
                try:
                    instance = Cart.objects.filter(user=request.user)
                    for book in books_list:
                        print("book",book)
                        to_del = CartItem.objects.get(cart=instance, book_id=book)
                        to_del.delete()
                    return Response({"msg": "Specific cart items deleted successfully"}, status=200)
                except Exception as ex:
                    print("ex",ex)
                    return Response({"msg": "Something went wrong"}, status=400)
        except  Exception as ex:
            print("ex",ex)
            return Response({"msg": "Something went wrong"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def get_cart(self, request, *args, **kwargs):
        try:
            try:
                instance = Cart.objects.get(user=request.user)
                print("instance", instance)
            except:
                instance = None
            if instance:

                # Check if the cart belongs to the current user (optional, depending on your logic)
                if instance.user != request.user:
                    return Response({"detail": "You do not have permission to delete this cart."},
                                    status=status.HTTP_403_FORBIDDEN)

                list_cart = CartSerializerResponse(instance,many=False).data
                return Response({"msg": "Cart get successfully","data":list_cart}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"msg": "Cart not found","data":[]}, status=status.HTTP_204_NO_CONTENT)

        except:
            return Response({"msg": "Something went wrong"}, status=status.HTTP_204_NO_CONTENT)



class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart_id=cart.id)

            if cart_items.exists():
                # Calculate total amount for the order
                total_amount = sum(item.quantity * item.price for item in cart_items)

                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total_amount
                )

                # Create order items from cart items
                order_items = []
                for cart_item in cart_items:
                    order_items.append(OrderItem(
                        order=order,
                        book=cart_item.book,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.price
                    ))

                # Bulk create order items for efficiency
                OrderItem.objects.bulk_create(order_items)

                # Optionally, clear cart items after creating the order
                cart_items.delete()

                return Response({"msg": "Order created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"msg": "Something went wrong!", "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_all_orders(self, request):
        try:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
            return Response({"msg": "Fetch order related data", "data": serializer.data})
        except Exception as ex:
            return Response({"msg": "Something went wrong!", "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)







