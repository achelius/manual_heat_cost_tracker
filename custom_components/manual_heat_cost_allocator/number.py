"""Number platform for Heat Cost Allocator."""
from homeassistant.components.number import NumberEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    prefix = config_entry.data.get("prefix", "")
    async_add_entities([HeatCostAllocatorNumber(hass, prefix)])

class HeatCostAllocatorNumber(NumberEntity):
    def __init__(self, hass, prefix):
        self.hass = hass
        self._prefix = prefix
        self._attr_name = f"{prefix} Heat Cost Allocator Set Value"
        self._attr_unique_id = f"{prefix}_heat_cost_allocator_set_value"
        self._attr_native_unit_of_measurement = "units"
        self._attr_native_value = 0

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = int(value)
        # Store the value in hass.data for the sensor to read
        if DOMAIN not in self.hass.data:
            self.hass.data[DOMAIN] = {}
        self.hass.data[DOMAIN]["current_value"] = self._attr_native_value
        self.async_write_ha_state()
        # Notify the sensor entity to update
        sensor = self.hass.data[DOMAIN].get("sensor_entity")
        if sensor:
            sensor.update_value(self._attr_native_value)
