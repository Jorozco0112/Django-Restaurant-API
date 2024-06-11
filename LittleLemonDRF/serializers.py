from rest_framework import serializers
from .models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory', read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    inventory = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'category', 'category_id', 'inventory']

    def validate_price(self, value):
        if value < 2:
            raise serializers.ValidationError('Price should not be less than 2.0')

        if value is None:
            raise serializers.ValidationError('Price is a required field')

        return value

    def validate_inventory(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative')

        return value
