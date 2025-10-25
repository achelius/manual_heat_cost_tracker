# Heat Cost Allocator Home Assistant Integration

This custom integration allows you to track the current value of an electronic heat cost allocator in Home Assistant.

## Features
- Sensor entity to track the current value
- Configurable via the Home Assistant UI

## Installation
1. Copy the `heat_cost_allocator` folder to your `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration via the Home Assistant UI.

## Configuration
No YAML configuration is required. Use the UI to set up the integration.

## File Overview
- `__init__.py`: Integration setup
- `manifest.json`: Integration metadata
- `const.py`: Constants
- `sensor.py`: Sensor platform
- `config_flow.py`: UI configuration flow
- `services.yaml`: Service descriptions
- `translations/`: UI translations
