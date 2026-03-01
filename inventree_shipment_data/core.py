"""Adds Weight and Volume to SO and exposes the data to reports"""

from plugin import InvenTreePlugin

from plugin.mixins import (
    EventMixin,
    ReportMixin,
    SettingsMixin,
    UrlsMixin,
    UserInterfaceMixin,
)

from . import PLUGIN_VERSION


class InvenTreeShipmentData(
    EventMixin,
    ReportMixin,
    SettingsMixin,
    UrlsMixin,
    UserInterfaceMixin,
    InvenTreePlugin,
):
    """InvenTreeShipmentData - custom InvenTree plugin."""

    # Plugin metadata
    TITLE = "InvenTree Shipment Data"
    NAME = "InvenTreeShipmentData"
    SLUG = "inventree-shipment-data"
    DESCRIPTION = "Adds Weight and Volume to SO and exposes the data to reports"
    VERSION = PLUGIN_VERSION

    # Additional project information
    AUTHOR = "gunstr"
    WEBSITE = "https://my-project-url.com"
    LICENSE = "MIT"

    # Optionally specify supported InvenTree versions
    # MIN_VERSION = '0.18.0'
    # MAX_VERSION = '2.0.0'

    # Render custom UI elements to the plugin settings page
    ADMIN_SOURCE = "Settings.js:renderPluginSettings"

    # Plugin settings (from SettingsMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/settings/
    SETTINGS = {
        # Define your plugin settings here...
        "CUSTOM_VALUE": {
            "name": "Custom Value",
            "description": "A custom value",
            "validator": int,
            "default": 42,
        }
    }

    # Respond to InvenTree events (from EventMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/event/
    def wants_process_event(self, event: str) -> bool:
        """Return True if the plugin wants to process the given event."""
        # Example: only process the 'create part' event
        return event == "part_part.created"

    def process_event(self, event: str, *args, **kwargs) -> None:
        """Process the provided event."""
        print("Processing custom event:", event)
        print("Arguments:", args)
        print("Keyword arguments:", kwargs)

    # Custom report context (from ReportMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/report/
    def add_label_context(
        self, label_instance, model_instance, request, context, **kwargs
    ):
        """Add custom context data to a label rendering context."""

        # Add custom context data to the label rendering context
        context["foo"] = "label_bar"

    def add_report_context(
        self, report_instance, model_instance, request, context, **kwargs
    ):
        """Add custom context data to a report rendering context."""

        # Add shipment data (weight/volume totals and units) for sales order reports
        from order.models import SalesOrder, SalesOrderShipment
        from .views import calculate_shipment_data, calculate_shipment_data_for_shipment

        if isinstance(model_instance, SalesOrder):
            try:
                data = calculate_shipment_data(model_instance)
                context["shipment_total_weight"] = data["total_weight"]
                context["shipment_total_volume"] = data["total_volume"]
                context["shipment_weight_unit"] = data["weight_unit"]
                context["shipment_volume_unit"] = data["volume_unit"]
            except Exception:
                # If calculation fails, just leave context as-is
                pass
        elif isinstance(model_instance, SalesOrderShipment):
            try:
                data = calculate_shipment_data_for_shipment(model_instance)
                context["shipment_total_weight"] = data["total_weight"]
                context["shipment_total_volume"] = data["total_volume"]
                context["shipment_weight_unit"] = data["weight_unit"]
                context["shipment_volume_unit"] = data["volume_unit"]
            except Exception:
                pass

    def report_callback(self, template, instance, report, request, **kwargs):
        """Callback function called after a report is generated."""
        ...

    # Custom URL endpoints (from UrlsMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/urls/
    def setup_urls(self):
        """Configure custom URL endpoints for this plugin."""
        from django.urls import path
        from .views import SalesOrderShipmentView, ShipmentShipmentView

        return [
            path(
                "salesorder/<int:pk>/shipment-data/",
                SalesOrderShipmentView.as_view(),
                name="so-shipment-data",
            ),
            path(
                "shipment/<int:pk>/shipment-data/",
                ShipmentShipmentView.as_view(),
                name="shipment-shipment-data",
            ),
        ]

    # User interface elements (from UserInterfaceMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/ui/

    # Custom UI panels
    def get_ui_panels(self, request, context: dict, **kwargs):
        """Return a list of custom panels to be rendered in the InvenTree user interface."""

        panels = []

        # Display this panel for either sales orders or individual shipments
        if context.get("target_model") in ["salesorder", "salesordershipment"]:
            panels.append({
                "key": "inventree-shipment-data-panel",
                "title": "Shipment Data",
                "description": "Displays weight/volume info for orders or shipments",
                "icon": "ti:truck",
                "source": self.plugin_static_file(
                    "Panel.js:renderInvenTreeShipmentDataPanel"
                ),
                "context": {
                    "settings": self.get_settings_dict(),
                    # additional context could be added here if needed
                },
            })

        return panels
