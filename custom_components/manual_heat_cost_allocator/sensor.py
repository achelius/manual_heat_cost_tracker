from .device import get_device_info
"""Sensor platform for Heat Cost Allocator."""
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Heat Cost Allocator sensor from a config entry."""
    prefix = config_entry.data.get("prefix", "")
    area_id = config_entry.data.get("area")
    sensor = HeatCostAllocatorSensor(hass, prefix, config_entry.entry_id, area_id)
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["sensor_entity"] = sensor
    async_add_entities([sensor])

class HeatCostAllocatorSensor(SensorEntity):
    """Representation of a Heat Cost Allocator sensor."""

    def __init__(self, hass, prefix, config_entry_id=None, area_id=None):
        self.hass = hass
        self._prefix = prefix
        self._config_entry_id = config_entry_id
        self._area_id = area_id
        self._attr_name = f"{prefix} Heat Cost Allocator Value"
        self._attr_unique_id = f"{prefix}_heat_cost_allocator_value"
        self._attr_native_unit_of_measurement = "units"
        self._attr_native_value = 0

    @property
    def device_info(self):
        return get_device_info(self._prefix, self._config_entry_id, self._area_id)

    @property
    def native_value(self):
        # Always read from hass.data if available
        value = self.hass.data.get(DOMAIN, {}).get("current_value")
        if value is not None:
            return int(value)
        return self._attr_native_value

    def update_value(self, value: int):
        self._attr_native_value = int(value)
        self.async_write_ha_state()
