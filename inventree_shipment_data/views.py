"""API views for the InvenTreeShipmentData plugin.

In practice, you would define your custom views here.

Ref: https://www.django-rest-framework.org/api-guide/views/
"""

from datetime import date
import random
import string

from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Parameter
from order.models import SalesOrder

from .serializers import ExampleSerializer, SalesOrderShipmentSerializer


class ExampleView(APIView):
    """Example API view for the InvenTreeShipmentData plugin.

    This view returns some very simple example data,
    but the concept can be extended to include more complex logic.
    """

    # You can control which users can access this view using DRF permissions
    permission_classes = [permissions.IsAuthenticated]

    # Control how the response is formatted
    serializer_class = ExampleSerializer

    def get(self, request, *args, **kwargs):
        """Override the GET method to return example data."""

        from part.models import Part

        response_serializer = self.serializer_class(
            data={
                "random_text": "".join(random.choices(string.ascii_letters, k=50)),
                "part_count": Part.objects.count(),
                "today": date.today(),
            }
        )

        # Serializer must be validated before it can be returned to the client
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=200)


class SalesOrderShipmentView(APIView):
    """Return weight/volume information for a given sales order."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SalesOrderShipmentSerializer

    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(SalesOrder, pk=pk)

        parts = []
        total_weight = 0.0
        total_volume = 0.0

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
                    elif name == "volume":
                        volume = float(p.data_numeric or 0)

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

        serializer = self.serializer_class(
            data={
                "parts": parts,
                "total_weight": total_weight,
                "total_volume": total_volume,
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
