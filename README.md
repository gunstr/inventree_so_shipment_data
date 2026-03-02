# InvenTreeShipmentData

Adds Weight and Volume to SO and exposes the data to reports.

The Plugin will use Volume and Weight parameters if available for parts in a Sales Order or allocated to a Sales Order Shipment. A panel will be added to Sales Orders and Sales Order Shipments where the values per row as well as for the complete Sales Order or Shipment can be instpected.

The plugin will also expose Total values to be used in report templates. Per row values can be calculated in directly in the template by accessing the same part parameters.

There is currenly no validation of units why it's important to freeze the unit in the parameter templates so the same Volume and Weight units are used for all parts in the system 

## Installation

### InvenTree Plugin Manager

Open the Plugin Manager and add this plugin with the following setting:

Package Name: `inventree_shipment_data`
Source URL: `git+https://github.com/gunstr/inventree_so_shipment_data.git`
Version: Select the version to install

Enable `Confirm plugin installation` and click Install

Once the installation is ready, activate the plugin

### Command Line 

To install manually via the command line, run the following command:

```bash
pip install git+https://github.com/gunstr/inventree_so_shipment_data
```

## Configuration

There are currently no configurations required for this Plugin.

## Usage

Add Volume and Weigth to each part where this is relevant.

In report templates the Totals can be accessd like this:

```html
Total Weight: {{ shipment_total_weight }} {{ shipment_weight_unit }}
Total Volume: {{ shipment_total_volume }} {{ shipment_volume_unit }}
```
