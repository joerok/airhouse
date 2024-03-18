from rest_framework import serializers

from shipment.models import Shipment, ShipmentItem


class ShipmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentItem
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    shipment_items = ShipmentItemSerializer(many=True)

    class Meta:
        model = Shipment
        fields = '__all__'
