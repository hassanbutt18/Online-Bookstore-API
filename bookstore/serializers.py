# serializers.py
from users.models import CustomUser
from rest_framework import serializers
from bookstore.models import Book ,Author ,Category ,Cart ,CartItem , Order, OrderItem
from rest_framework.exceptions import ValidationError




class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        # Custom update method to update an existing Book instance
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

class BookSerializerResponse(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        author = Author.objects.create(name=validated_data.get('name'),created_by=self.context.get('user'))
        return author

    def update(self, instance, validated_data):
        # Custom update method to update an existing Author instance
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class UserSerializerResponse(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'

class AuthorSerializerResponse(serializers.ModelSerializer):
    created_by = UserSerializerResponse(many=False)

    class Meta:
        model = Author
        fields = ['id','name','created_by','created_at']




class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        author = Category.objects.create(name=validated_data.get('name'),created_by=self.context.get('user'))
        return author

    def update(self, instance, validated_data):
        # Custom update method to update an existing Author instance
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class CartSerializer(serializers.Serializer):

    class Meta:
        model = Cart
        fields = "__all__"

    def create(self, validated_data):

        user = self.context.get('user')
        items = self.context.get('items')
        cart = Cart.objects.create(user=user)
        for item in items:
            CartItem.objects.create(cart_id=cart.id, book_id=item['book'],quantity=item['quantity'],price=item['price'])
        return cart

    def update(self, instance, validated_data):
        # Custom update method to update an existing Book instance
        items = self.context.get('items')
        print("items",items)
        for item in items:
            if CartItem.objects.filter(cart_id=instance.id, book_id=item['book'], quantity=item['quantity']).exists():
                pass
            else:
                a = CartItem.objects.create(cart_id=instance.id, book_id=item['book'], quantity=item['quantity'],price=item['price'])
                print("asd",a)
        return instance



class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializerResponse(serializers.ModelSerializer):
    items = CartItemsSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id','items']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','book','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','order_items','total_amount','created_at','user']
