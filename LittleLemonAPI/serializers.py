from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import *
from rest_framework.validators import UniqueValidator
import bleach
from django.contrib.auth import get_user_model

# User = get_user_model()

class UserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'group')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
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
        fields = ["id", "title", "price", "inventory", "featured", "category", "category_id"]
        extra_kwargs = {
            "price": {'min_value': 2},
            "inventory": {'min_value': 0},
        }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
