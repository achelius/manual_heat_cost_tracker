"""Sensor platform for Heat Cost Allocator."""
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Heat Cost Allocator sensor from a config entry."""
    prefix = config_entry.data.get("prefix", "")
    sensor = HeatCostAllocatorSensor(hass, prefix)
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["sensor_entity"] = sensor
    async_add_entities([sensor])

class HeatCostAllocatorSensor(SensorEntity):
    """Representation of a Heat Cost Allocator sensor."""

    def __init__(self, hass, prefix):
        self.hass = hass
        self._prefix = prefix
        self._attr_name = f"{prefix} Heat Cost Allocator Value"
        self._attr_unique_id = f"{prefix}_heat_cost_allocator_value"
        self._attr_native_unit_of_measurement = "units"
        self._attr_native_value = 0

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
