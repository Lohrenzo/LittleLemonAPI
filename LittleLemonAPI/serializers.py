from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import *
from rest_framework.validators import UniqueValidator
import bleach
from django.contrib.auth import get_user_model


class UserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'group')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all()
    )
    # category_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        max_length=255, 
        validators = [UniqueValidator(queryset=MenuItem.objects.all())]
    ) # Unique Validator for title. 1st Method

    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title']) # Uses bleach to sanitize/clean up the title field. Method 1
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)

    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "inventory", "featured", "category"]
        extra_kwargs = {
            "price": {'min_value': 2},
            "inventory": {'min_value': 0},
        }

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    
    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }
  

class OrderItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    name = serializers.CharField(source='menuitem.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'menuitem': {'read_only': True}
        }


class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')
    
    class Meta:
        model = Order
        fields = '__all__'

