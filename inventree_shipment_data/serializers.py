"""API serializers for the InvenTreeShipmentData plugin.

Only serializers required by the shipment data panel are defined here.
"""

from rest_framework import serializers


# --- new serializers for sales order shipment data ---
class PartShipmentSerializer(serializers.Serializer):
    part_id = serializers.IntegerField(allow_null=True)
    part_name = serializers.CharField(allow_null=True)
    quantity = serializers.FloatField()
    weight = serializers.FloatField(allow_null=True)
    volume = serializers.FloatField(allow_null=True)
    line_weight = serializers.FloatField()
    line_volume = serializers.FloatField()


class SalesOrderShipmentSerializer(serializers.Serializer):
    parts = PartShipmentSerializer(many=True)
    total_weight = serializers.FloatField()
    total_volume = serializers.FloatField()
