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

        # Add custom context data to the report rendering context
        context["foo"] = "report_bar"

    def report_callback(self, template, instance, report, request, **kwargs):
        """Callback function called after a report is generated."""
        ...

    # Custom URL endpoints (from UrlsMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/urls/
    def setup_urls(self):
        """Configure custom URL endpoints for this plugin."""
        from django.urls import path
        from .views import ExampleView

        return [
            # Provide path to a simple custom view - replace this with your own views
            path("example/", ExampleView.as_view(), name="example-view"),
        ]

    # User interface elements (from UserInterfaceMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/ui/

    # Custom UI panels
    def get_ui_panels(self, request, context: dict, **kwargs):
        """Return a list of custom panels to be rendered in the InvenTree user interface."""

        panels = []

        # Only display this panel for the 'part' target
        if context.get("target_model") == "part":
            panels.append({
                "key": "inventree-shipment-data-panel",
                "title": "InvenTree Shipment Data",
                "description": "Custom panel description",
                "icon": "ti:mood-smile:outline",
                "source": self.plugin_static_file(
                    "Panel.js:renderInvenTreeShipmentDataPanel"
                ),
                "context": {
                    # Provide additional context data to the panel
                    "settings": self.get_settings_dict(),
                    "foo": "bar",
                },
            })

        return panels
