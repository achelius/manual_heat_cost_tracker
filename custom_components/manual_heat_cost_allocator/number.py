from .device import get_device_info
"""Number platform for Heat Cost Allocator."""
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.storage import Store
from .const import DOMAIN

METER_STORE_KEY = "manual_heat_cost_allocator.meter_values"

async def async_setup_entry(hass, config_entry, async_add_entities):
    prefix = config_entry.data.get("prefix", "")
    area_id = config_entry.data.get("area")
    # Load stored values
    store = Store(hass, 1, METER_STORE_KEY)
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if "values" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["values"] = {}
    stored = await store.async_load() or {}
    hass.data[DOMAIN]["values"].update(stored)
    hass.data[DOMAIN]["store"] = store
    async_add_entities([HeatCostAllocatorNumber(hass, prefix, config_entry.entry_id, area_id)])

class HeatCostAllocatorNumber(NumberEntity):
    def __init__(self, hass, prefix, config_entry_id=None, area_id=None):
        self.hass = hass
        self._prefix = prefix
        self._config_entry_id = config_entry_id
        self._area_id = area_id
        self._attr_name = f"{prefix} Heat Cost Allocator Set Value"
        self._attr_unique_id = f"{prefix}_heat_cost_allocator_set_value"
        self._attr_native_unit_of_measurement = "units"
        self._attr_native_value = 0
        self._attr_mode = "box"  # Use numeric up/down instead of slider
        self._attr_native_min_value = 0
        self._attr_native_max_value = 999999
        self._attr_native_step = 1
        self._attr_device_class = None
        self._attr_state_class = None

    @property
    def device_info(self):
        return get_device_info(self._prefix, self._config_entry_id, self._area_id)

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = int(value)
        # Store the value in hass.data for the sensor to read, per device
        if DOMAIN not in self.hass.data:
            self.hass.data[DOMAIN] = {}
        if "values" not in self.hass.data[DOMAIN]:
            self.hass.data[DOMAIN]["values"] = {}
        self.hass.data[DOMAIN]["values"][self._config_entry_id] = self._attr_native_value
        # Persist values
        store = self.hass.data[DOMAIN].get("store")
        if store:
            await store.async_save(self.hass.data[DOMAIN]["values"])
        self.async_write_ha_state()
        # Notify the sensor entity to update
        sensor = self.hass.data[DOMAIN].get("sensor_entity")
        if sensor and getattr(sensor, '_config_entry_id', None) == self._config_entry_id:
            sensor.update_value(self._attr_native_value)

    @property
    def native_value(self):
        # Return the value for this device
        value = None
        if DOMAIN in self.hass.data and "values" in self.hass.data[DOMAIN]:
            value = self.hass.data[DOMAIN]["values"].get(self._config_entry_id)
        if value is not None:
            return int(value)
        return int(self._attr_native_value)
