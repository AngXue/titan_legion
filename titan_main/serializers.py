from rest_framework import serializers

from .models import Profile, Item, Order, Apply


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = '__all__'
