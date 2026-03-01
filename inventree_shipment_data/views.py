"""API views for the InvenTreeShipmentData plugin.

In practice, you would define your custom views here.

Ref: https://www.django-rest-framework.org/api-guide/views/
"""

from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Parameter
from order.models import SalesOrder

from .serializers import SalesOrderShipmentSerializer


def calculate_shipment_data(order: SalesOrder):
    """Calculate weight and volume totals for a sales order.

    Returns a dict with parts list, totals, and units.
    """
    parts = []
    total_weight = 0.0
    total_volume = 0.0
    weight_unit = None
    volume_unit = None

    for line in order.lines.select_related("part").all():
        part = line.part
        qty = float(line.quantity or 0)

        weight = 0.0
        volume = 0.0

        if part:
            qs = Parameter.objects.filter(
                model_type__app_label="part",
                model_id=part.pk,
                template__name__in=["Weight", "Volume"],
            ).select_related("template")

            for p in qs:
                name = p.template.name.lower()
                if name == "weight":
                    weight = float(p.data_numeric or 0)
                    if weight_unit is None:
                        weight_unit = p.template.units
                elif name == "volume":
                    volume = float(p.data_numeric or 0)
                    if volume_unit is None:
                        volume_unit = p.template.units

        line_weight = weight * qty
        line_volume = volume * qty

        total_weight += line_weight
        total_volume += line_volume

        parts.append({
            "part_id": part.pk if part else None,
            "part_name": part.name if part else None,
            "quantity": qty,
            "weight": weight or None,
            "volume": volume or None,
            "line_weight": line_weight,
            "line_volume": line_volume,
        })

    return {
        "parts": parts,
        "total_weight": total_weight,
        "total_volume": total_volume,
        "weight_unit": weight_unit,
        "volume_unit": volume_unit,
    }


class SalesOrderShipmentView(APIView):
    """Return weight/volume information for a given sales order."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SalesOrderShipmentSerializer

    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(SalesOrder, pk=pk)
        data = calculate_shipment_data(order)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
