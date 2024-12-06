from rest_framework import serializers

from .models import Profile, Item, Order, Apply


def validate_value(value, _range):
    if value < _range[0] or value > _range[1]:
        raise serializers.ValidationError(f"{value}: 超出范围[{_range[0]}, {_range[1]}]！")
    return value


class ProfileSerializer(serializers.ModelSerializer):
    __str__ = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'character_id', 'nickname', 'pap', 'isk', 'skill', 
                 'lp', 'used_lp', 'user', '__str__']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    def validate_item_price(self, value):
        range_value = (0, 999)
        return validate_value(value, range_value)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_lp_cost(self, value):
        range_value = (0, 999)
        return validate_value(value, range_value)

    def validate_item_quantity(self, value):
        range_value = (1, 999)
        return validate_value(value, range_value)


class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = '__all__'
